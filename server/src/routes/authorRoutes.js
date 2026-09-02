import express from 'express';
import Course from '../models/Course.js';
import { authenticateToken, requireAdmin } from '../middleware/auth.js';

const router = express.Router();

// Require authenticated admin/author for all authoring endpoints
router.use(authenticateToken);
router.use(requireAdmin);

// Create new Course
router.post('/courses', async (req, res) => {
  try {
    const { title, description, category, level, accent } = req.body;
    const newCourse = await Course.create({
      title,
      description,
      category: category || 'General',
      level: level || 'Beginner',
      accent: accent || 'blue',
      lessons: []
    });
    res.status(201).json(newCourse);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// Add Lesson with LCM parameters to Course
router.post('/courses/:courseId/lessons', async (req, res) => {
  try {
    const { courseId } = req.params;
    const course = await Course.findById(courseId);
    if (!course) return res.status(404).json({ message: 'Course not found' });

    const newLesson = {
      title: req.body.title,
      summary: req.body.summary,
      content: req.body.content || req.body.summary,
      videoUrl: req.body.videoUrl || req.body.led?.videoUrl || '',
      durationMinutes: req.body.durationMinutes || 10,
      order: course.lessons.length + 1,
      led: req.body.led || {},
      lbd: req.body.lbd || {},
      lxt: req.body.lxt || [],
      lxi: req.body.lxi || {}
    };

    course.lessons.push(newLesson);
    await course.save();
    res.status(201).json(course);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// Update Lesson LCM parameters
router.put('/courses/:courseId/lessons/:lessonId', async (req, res) => {
  try {
    const { courseId, lessonId } = req.params;
    const course = await Course.findById(courseId);
    if (!course) return res.status(404).json({ message: 'Course not found' });

    const lesson = course.lessons.id(lessonId);
    if (!lesson) return res.status(404).json({ message: 'Lesson not found' });

    // Update fields
    if (req.body.title) lesson.title = req.body.title;
    if (req.body.summary !== undefined) lesson.summary = req.body.summary;
    if (req.body.content !== undefined) lesson.content = req.body.content;
    if (req.body.videoUrl !== undefined) lesson.videoUrl = req.body.videoUrl;
    if (req.body.durationMinutes !== undefined) lesson.durationMinutes = req.body.durationMinutes;

    if (req.body.led) lesson.led = req.body.led;
    if (req.body.lbd) lesson.lbd = req.body.lbd;
    if (req.body.lxt) lesson.lxt = req.body.lxt;
    if (req.body.lxi) lesson.lxi = req.body.lxi;

    await course.save();
    res.json(course);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// Delete Lesson
router.delete('/courses/:courseId/lessons/:lessonId', async (req, res) => {
  try {
    const { courseId, lessonId } = req.params;
    const course = await Course.findById(courseId);
    if (!course) return res.status(404).json({ message: 'Course not found' });

    course.lessons.pull(lessonId);
    await course.save();
    res.json(course);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

export default router;
