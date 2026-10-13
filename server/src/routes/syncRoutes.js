import express from 'express';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import mongoose from 'mongoose';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const DATA_DIR = path.resolve(__dirname, '../../data');
const COURSES_FILE = path.join(DATA_DIR, 'courses.json');
const DRAFT_FILE = path.join(DATA_DIR, 'draft_courses.json');

const curriculumSchema = new mongoose.Schema({
  key: { type: String, required: true, unique: true },
  courses: { type: Array, default: [] }
}, { timestamps: true });

const CurriculumModel = mongoose.models.CurriculumSync || mongoose.model('CurriculumSync', curriculumSchema);

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
router.get('/courses', async (req, res) => {
  if (mongoose.connection.readyState === 1) {
    try {
      const doc = await CurriculumModel.findOne({ key: 'published' });
      if (doc && Array.isArray(doc.courses) && doc.courses.length > 0) {
        return res.json({ success: true, count: doc.courses.length, data: doc.courses });
      }
      // If MongoDB is connected but empty, seed from local courses.json
      const localCourses = readJsonFile(COURSES_FILE, []);
      if (localCourses.length > 0) {
        await CurriculumModel.findOneAndUpdate({ key: 'published' }, { courses: localCourses }, { upsert: true });
        return res.json({ success: true, count: localCourses.length, data: localCourses });
      }
    } catch (e) {
      console.warn('MongoDB query warning in courses:', e.message);
    }
  }

  const courses = readJsonFile(COURSES_FILE, []);
  res.json({ success: true, count: courses.length, data: courses });
});

// GET /api/v2/courses/draft - Get draft courses
router.get('/courses/draft', async (req, res) => {
  if (mongoose.connection.readyState === 1) {
    try {
      const doc = await CurriculumModel.findOne({ key: 'draft' });
      if (doc && Array.isArray(doc.courses) && doc.courses.length > 0) {
        return res.json({ success: true, count: doc.courses.length, data: doc.courses });
      }
    } catch (e) {
      console.warn('MongoDB query warning in draft courses:', e.message);
    }
  }

  let drafts = readJsonFile(DRAFT_FILE, null);
  if (!drafts) {
    drafts = readJsonFile(COURSES_FILE, []);
  }
  res.json({ success: true, count: drafts.length, data: drafts });
});

// POST /api/v2/courses/draft - Save author draft courses
router.post('/courses/draft', async (req, res) => {
  const { courses } = req.body;
  if (!courses || !Array.isArray(courses)) {
    return res.status(400).json({ success: false, message: 'Invalid payload: "courses" array is required.' });
  }

  if (mongoose.connection.readyState === 1) {
    try {
      await CurriculumModel.findOneAndUpdate({ key: 'draft' }, { courses }, { upsert: true });
    } catch (e) {
      console.warn('MongoDB save warning in draft courses:', e.message);
    }
  }

  writeJsonFile(DRAFT_FILE, courses);
  res.json({ success: true, message: 'Draft saved successfully.', count: courses.length });
});

// POST /api/v2/courses/publish - Publish draft to live
router.post('/courses/publish', async (req, res) => {
  const { courses } = req.body;
  let toPublish = courses;
  if (!toPublish || !Array.isArray(toPublish)) {
    toPublish = readJsonFile(DRAFT_FILE, null);
  }
  if (!toPublish || !Array.isArray(toPublish)) {
    return res.status(400).json({ success: false, message: 'No courses provided or draft found to publish.' });
  }

  if (mongoose.connection.readyState === 1) {
    try {
      await CurriculumModel.findOneAndUpdate({ key: 'published' }, { courses: toPublish }, { upsert: true });
      await CurriculumModel.findOneAndUpdate({ key: 'draft' }, { courses: toPublish }, { upsert: true });
    } catch (e) {
      console.warn('MongoDB save warning in publish courses:', e.message);
    }
  }

  writeJsonFile(COURSES_FILE, toPublish);
  writeJsonFile(DRAFT_FILE, toPublish);
  res.json({ success: true, message: 'Courses published live to students!', count: toPublish.length, data: toPublish });
});

// POST /api/v2/courses/reset - Reset courses to default seed
router.post('/courses/reset', async (req, res) => {
  const defaultCourses = readJsonFile(COURSES_FILE, []);
  if (mongoose.connection.readyState === 1) {
    try {
      await CurriculumModel.findOneAndUpdate({ key: 'draft' }, { courses: defaultCourses }, { upsert: true });
    } catch (e) {}
  }
  writeJsonFile(DRAFT_FILE, defaultCourses);
  res.json({ success: true, message: 'Draft reset to published.', data: defaultCourses });
});

export default router;
