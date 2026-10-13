import express from 'express';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import mongoose from 'mongoose';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const DATA_DIR = path.resolve(__dirname, '../../data');
const ATTEMPTS_FILE = path.join(DATA_DIR, 'attempts.json');

const attemptSchema = new mongoose.Schema({
  id: { type: String, index: true },
  traineeId: String,
  traineeName: String,
  questionId: String,
  moduleId: String,
  submoduleId: String,
  selectedChoice: mongoose.Schema.Types.Mixed,
  isCorrect: Boolean,
  attemptsCount: Number,
  hintsUsed: Number,
  timeSpentSeconds: Number,
  timestamp: String
}, { timestamps: true, strict: false });

const AttemptModel = mongoose.models.QuizAttemptV2 || mongoose.model('QuizAttemptV2', attemptSchema);

const router = express.Router();

function readJsonFile(filePath, fallback = []) {
  try {
    if (!fs.existsSync(filePath)) {
      return fallback;
    }
    const raw = fs.readFileSync(filePath, 'utf-8');
    return JSON.parse(raw);
  } catch (err) {
    console.error(`Error reading ${filePath}:`, err.message);
    return fallback;
  }
}

function writeJsonFile(filePath, data) {
  try {
    if (!fs.existsSync(DATA_DIR)) {
      fs.mkdirSync(DATA_DIR, { recursive: true });
    }
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf-8');
    return true;
  } catch (err) {
    console.error(`Error writing ${filePath}:`, err.message);
    return false;
  }
}

// GET /api/v2/attempts - Retrieve all attempts for the Admin Dashboard
router.get('/', async (req, res) => {
  if (mongoose.connection.readyState === 1) {
    try {
      const dbAttempts = await AttemptModel.find().sort({ createdAt: -1 });
      if (dbAttempts && dbAttempts.length > 0) {
        return res.json({ success: true, count: dbAttempts.length, data: dbAttempts });
      }
    } catch (e) {
      console.warn('MongoDB query warning in attempts:', e.message);
    }
  }

  const attempts = readJsonFile(ATTEMPTS_FILE, []);
  res.json({ success: true, count: attempts.length, data: attempts });
});

// POST /api/v2/attempts - Record a new attempt from student/companion
router.post('/', async (req, res) => {
  const attempt = req.body;
  if (!attempt || !attempt.questionId) {
    return res.status(400).json({ success: false, message: 'Invalid attempt payload.' });
  }

  const attempts = readJsonFile(ATTEMPTS_FILE, []);
  const newAttempt = {
    id: attempt.id || `att-${Date.now()}-${Math.floor(Math.random() * 1000)}`,
    timestamp: attempt.timestamp || 'Just Now',
    ...attempt
  };

  if (mongoose.connection.readyState === 1) {
    try {
      await AttemptModel.create(newAttempt);
    } catch (e) {
      console.warn('MongoDB save warning in attempts:', e.message);
    }
  }

  attempts.unshift(newAttempt);
  writeJsonFile(ATTEMPTS_FILE, attempts);
  res.status(201).json({ success: true, data: newAttempt });
});

// POST /api/v2/attempts/reset - Reset attempts to seed
router.post('/reset', async (req, res) => {
  if (mongoose.connection.readyState === 1) {
    try {
      await AttemptModel.deleteMany({});
    } catch (e) {}
  }
  writeJsonFile(ATTEMPTS_FILE, []);
  res.json({ success: true, message: 'Attempts cleared.' });
});

export default router;
