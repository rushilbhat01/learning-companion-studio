import express from 'express';
import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import mongoose from 'mongoose';
import User from '../models/User.js';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const DATA_DIR = path.resolve(__dirname, '../../data');
const USERS_FILE = path.join(DATA_DIR, 'users.json');
const JWT_SECRET = process.env.JWT_SECRET || 'lcs-mentorship-secret-key-2026';

const router = express.Router();

function readJsonFile(filePath, fallback = []) {
  try {
    if (!fs.existsSync(filePath)) return fallback;
    const raw = fs.readFileSync(filePath, 'utf-8');
    return JSON.parse(raw);
  } catch (err) {
    console.error(`Error reading ${filePath}:`, err.message);
    return fallback;
  }
}

function writeJsonFile(filePath, data) {
  try {
    if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf-8');
    return true;
  } catch (err) {
    console.error(`Error writing ${filePath}:`, err.message);
    return false;
  }
}

function hashSha256(password) {
  return crypto.createHash('sha256').update(password).digest('hex');
}

// Ensure default author account exists in local and MongoDB storage
async function ensureAuthorSeeded() {
  const users = readJsonFile(USERS_FILE, []);
  const authorExists = users.some(u => u.role === 'author' || u.email.toLowerCase() === 'author@imlc.org');
  const salt = bcrypt.genSaltSync(10);
  const hash = bcrypt.hashSync("Author@IMLC2026", salt);

  if (!authorExists) {
    const authorUser = {
      id: "AUTH-001",
      name: "Lead Author",
      email: "author@imlc.org",
      passwordHash: hash,
      role: "author",
      createdAt: new Date().toISOString()
    };
    users.unshift(authorUser);
    writeJsonFile(USERS_FILE, users);
  }

  // Also seed MongoDB if connected
  if (mongoose.connection.readyState === 1) {
    try {
      const dbAuthor = await User.findOne({ email: "author@imlc.org" });
      if (!dbAuthor) {
        await User.create({
          customId: "AUTH-001",
          name: "Lead Author",
          email: "author@imlc.org",
          passwordHash: hash,
          role: "author"
        });
      }
    } catch (e) {
      // Ignore background seed race
    }
  }
}

ensureAuthorSeeded();

// POST /api/v2/auth/login
router.post('/login', async (req, res) => {
  try {
    const { email, password } = req.body;
    if (!email || !password) {
      return res.status(400).json({ success: false, message: 'Email and password are required.' });
    }

    const cleanEmail = email.toLowerCase().trim();
    let user = null;

    // 1. Check MongoDB first if connected
    if (mongoose.connection.readyState === 1) {
      try {
        const query = (cleanEmail === 'author')
          ? { role: 'author' }
          : { email: cleanEmail };
        const dbUser = await User.findOne(query).select('+passwordHash');
        if (dbUser) {
          user = {
            id: dbUser.customId || dbUser._id.toString(),
            name: dbUser.name,
            email: dbUser.email,
            passwordHash: dbUser.passwordHash,
            role: dbUser.role
          };
        }
      } catch (err) {
        console.warn('MongoDB query warning, using file fallback:', err.message);
      }
    }

    // 2. Check JSON file storage if not found in MongoDB
    if (!user) {
      const users = readJsonFile(USERS_FILE, []);
      user = users.find(u => 
        u.email.toLowerCase() === cleanEmail || 
        (u.role === 'author' && cleanEmail === 'author')
      );
    }

    if (!user) {
      return res.status(401).json({ success: false, message: 'Invalid email or password.' });
    }

    // Verify password via bcrypt or legacy hash
    let isMatch = false;
    if (user.passwordHash && user.passwordHash.startsWith('$2')) {
      isMatch = await bcrypt.compare(password, user.passwordHash);
    } else if (user.passwordHash) {
      isMatch = (user.passwordHash === hashSha256(password));
    } else if (user.password) {
      isMatch = (user.password === password);
    }

    // Check fixed author fallback
    if (!isMatch && (cleanEmail === 'author@imlc.org' || cleanEmail === 'author') && password === 'Author@IMLC2026') {
      isMatch = true;
    }

    if (!isMatch) {
      return res.status(401).json({ success: false, message: 'Invalid email or password.' });
    }

    // Sign JWT Token
    const token = jwt.sign(
      { id: user.id, email: user.email, role: user.role, name: user.name },
      JWT_SECRET,
      { expiresIn: '14d' }
    );

    const { password: _, passwordHash: __, ...safeUser } = user;
    res.json({
      success: true,
      token,
      data: { ...safeUser, token }
    });
  } catch (err) {
    console.error('Login Error:', err);
    res.status(500).json({ success: false, message: 'Internal authentication server error.' });
  }
});

// POST /api/v2/auth/register
router.post('/register', async (req, res) => {
  try {
    const { name, email, password, role } = req.body;
    if (!name || !email || !password) {
      return res.status(400).json({ success: false, message: 'Name, email, and password are required.' });
    }
    if (password.length < 6) {
      return res.status(400).json({ success: false, message: 'Password must be at least 6 characters.' });
    }

    if (role === 'author') {
      return res.status(403).json({ success: false, message: 'Author accounts cannot be registered. Use existing author credentials to sign in.' });
    }

    const cleanEmail = email.toLowerCase().trim();
    const users = readJsonFile(USERS_FILE, []);

    // Check MongoDB for duplicate email
    if (mongoose.connection.readyState === 1) {
      const existingDb = await User.findOne({ email: cleanEmail });
      if (existingDb) {
        return res.status(409).json({ success: false, message: 'An account with this email address already exists.' });
      }
    }

    // Check JSON file storage for duplicate email
    if (users.find(u => u.email.toLowerCase() === cleanEmail)) {
      return res.status(409).json({ success: false, message: 'An account with this email address already exists.' });
    }

    // Securely hash password with bcrypt
    const salt = await bcrypt.genSalt(10);
    const passwordHash = await bcrypt.hash(password, salt);

    const year = new Date().getFullYear();
    const randId = Math.floor(1000 + Math.random() * 9000);
    const customId = `LC-${year}-${randId}`;

    const newUser = {
      id: customId,
      name: name.trim(),
      email: cleanEmail,
      passwordHash: passwordHash,
      role: 'companion',
      createdAt: new Date().toISOString()
    };

    // Save to MongoDB if connected
    if (mongoose.connection.readyState === 1) {
      try {
        const doc = await User.create({
          customId,
          name: name.trim(),
          email: cleanEmail,
          passwordHash,
          role: 'companion'
        });
        newUser.id = doc.customId || doc._id.toString();
      } catch (err) {
        console.warn('MongoDB save warning, fallback to file:', err.message);
      }
    }

    // Always update JSON backup file
    users.push(newUser);
    writeJsonFile(USERS_FILE, users);

    // Sign JWT Token
    const token = jwt.sign(
      { id: newUser.id, email: newUser.email, role: newUser.role, name: newUser.name },
      JWT_SECRET,
      { expiresIn: '14d' }
    );

    const { passwordHash: __, ...safeUser } = newUser;
    res.status(201).json({
      success: true,
      token,
      data: { ...safeUser, token }
    });
  } catch (err) {
    console.error('Registration Error:', err);
    res.status(500).json({ success: false, message: 'Internal registration server error.' });
  }
});

// GET /api/v2/auth/users
router.get('/users', async (_req, res) => {
  if (mongoose.connection.readyState === 1) {
    try {
      const dbUsers = await User.find().select('-passwordHash');
      return res.json({ success: true, count: dbUsers.length, data: dbUsers });
    } catch (e) {
      // fallback
    }
  }
  const users = readJsonFile(USERS_FILE, []);
  const safeUsers = users.map(({ password, passwordHash, ...rest }) => rest);
  res.json({ success: true, count: safeUsers.length, data: safeUsers });
});

export default router;
