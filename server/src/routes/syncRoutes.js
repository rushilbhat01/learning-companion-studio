import express from 'express';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const DATA_DIR = path.resolve(__dirname, '../../data');
const COURSES_FILE = path.join(DATA_DIR, 'courses.json');
const DRAFT_FILE = path.join(DATA_DIR, 'draft_courses.json');

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

// Ensure files exist
if (!fs.existsSync(COURSES_FILE)) {
  writeJsonFile(COURSES_FILE, []);
}

// GET /api/v2/courses - Get published courses
router.get('/courses', (req, res) => {
  const courses = readJsonFile(COURSES_FILE, []);
  res.json({ success: true, count: courses.length, data: courses });
});

// GET /api/v2/courses/draft - Get draft courses
router.get('/courses/draft', (req, res) => {
  let drafts = readJsonFile(DRAFT_FILE, null);
  if (!drafts) {
    drafts = readJsonFile(COURSES_FILE, []);
  }
  res.json({ success: true, count: drafts.length, data: drafts });
});

// POST /api/v2/courses/draft - Save author draft courses
router.post('/courses/draft', (req, res) => {
  const { courses } = req.body;
  if (!courses || !Array.isArray(courses)) {
    return res.status(400).json({ success: false, message: 'Invalid payload: "courses" array is required.' });
  }
  writeJsonFile(DRAFT_FILE, courses);
  res.json({ success: true, message: 'Draft saved successfully.', count: courses.length });
});

// POST /api/v2/courses/publish - Publish draft to live
router.post('/courses/publish', (req, res) => {
  const { courses } = req.body;
  let toPublish = courses;
  if (!toPublish || !Array.isArray(toPublish)) {
    toPublish = readJsonFile(DRAFT_FILE, null);
  }
  if (!toPublish || !Array.isArray(toPublish)) {
    return res.status(400).json({ success: false, message: 'No courses provided or draft found to publish.' });
  }

  writeJsonFile(COURSES_FILE, toPublish);
  writeJsonFile(DRAFT_FILE, toPublish);
  res.json({ success: true, message: 'Courses published live to students!', count: toPublish.length, data: toPublish });
});

// POST /api/v2/courses/reset - Reset courses to default seed
router.post('/courses/reset', (req, res) => {
  const defaultCourses = readJsonFile(COURSES_FILE, []);
  writeJsonFile(DRAFT_FILE, defaultCourses);
  res.json({ success: true, message: 'Draft reset to published.', data: defaultCourses });
});

export default router;
