import express from 'express';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const DATA_DIR = path.resolve(__dirname, '../../data');
const EVENTS_FILE = path.join(DATA_DIR, 'events.json');

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

// POST /api/v2/events - Log a user movement or telemetry action
router.post('/', (req, res) => {
  const event = req.body;
  if (!event || !event.eventType) {
    return res.status(400).json({ success: false, message: 'Invalid payload: eventType required.' });
  }

  const events = readJsonFile(EVENTS_FILE, []);
  const newEvent = {
    id: event.id || `evt-${Date.now()}-${Math.floor(Math.random() * 1000)}`,
    timestamp: event.timestamp || new Date().toISOString(),
    ...event
  };

  events.unshift(newEvent);
  if (events.length > 5000) events.length = 5000;
  writeJsonFile(EVENTS_FILE, events);

  res.status(201).json({ success: true, data: newEvent });
});

// GET /api/v2/events - Retrieve events, optionally filtered
router.get('/', (req, res) => {
  const events = readJsonFile(EVENTS_FILE, []);
  const { userId, eventType, limit } = req.query;

  let filtered = events;
  if (userId && userId !== 'ALL') {
    filtered = filtered.filter(e => e.userId === userId || e.userName === userId);
  }
  if (eventType && eventType !== 'ALL') {
    filtered = filtered.filter(e => e.eventType === eventType);
  }
  if (limit) {
    filtered = filtered.slice(0, parseInt(limit, 10));
  }

  res.json({ success: true, count: filtered.length, data: filtered });
});

const PRESENCE_FILE = path.join(DATA_DIR, 'presence.json');

// POST /api/v2/events/presence - Record user presence heartbeat
router.post('/presence', (req, res) => {
  const { userId, name, role, lastActivity, online } = req.body;
  if (!userId) {
    return res.status(400).json({ success: false, message: 'userId required.' });
  }

  const presenceMap = readJsonFile(PRESENCE_FILE, {});
  presenceMap[userId] = {
    userId,
    name: name || userId,
    role: role || 'companion',
    lastHeartbeat: Date.now(),
    lastActivity: lastActivity || 'Active on site',
    online: online !== false
  };

  writeJsonFile(PRESENCE_FILE, presenceMap);
  res.json({ success: true, data: presenceMap[userId] });
});

// GET /api/v2/events/presence - Retrieve all users' presence statuses
router.get('/presence', (_req, res) => {
  const presenceMap = readJsonFile(PRESENCE_FILE, {});
  const now = Date.now();
  const list = Object.values(presenceMap).map(u => ({
    ...u,
    isOnline: u.online && (now - u.lastHeartbeat < 35000)
  }));
  res.json({ success: true, count: list.length, data: list });
});

// POST /api/v2/events/reset
router.post('/reset', (_req, res) => {
  writeJsonFile(EVENTS_FILE, []);
  res.json({ success: true, message: 'Movement logs cleared.' });
});

export default router;
