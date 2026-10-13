import 'dotenv/config';
import express from 'express';
import cors from 'cors';
import morgan from 'morgan';
import { connectDatabase } from './config/db.js';
import authRoutes from './routes/authRoutes.js';
import courseRoutes from './routes/courseRoutes.js';
import eventRoutes from './routes/eventRoutes.js';
import analyticsRoutes from './routes/analyticsRoutes.js';
import authorRoutes from './routes/authorRoutes.js';
import syncRoutes from './routes/syncRoutes.js';
import attemptsRoutes from './routes/attemptsRoutes.js';

const app = express();

// Allow all origins (localhost + file://)
app.use(cors({
  origin: true,
  credentials: true
}));

app.use(express.json({ limit: '10mb' }));
app.use(morgan('dev'));

// API Health Check
app.get('/api/health', (_req, res) => res.json({ 
  status: 'ok', 
  service: 'Learning Companion Studio API',
  mode: 'fullstack',
  timestamp: new Date().toISOString()
}));

// Classic REST Routes
app.use('/api/auth', authRoutes);
app.use('/api/courses', courseRoutes);
app.use('/api/events', eventRoutes);
app.use('/api/analytics', analyticsRoutes);
app.use('/api/author', authorRoutes);

// V2 Full-State Sync & Real-Time Attempt Routes
app.use('/api/v2', syncRoutes);
app.use('/api/v2/attempts', attemptsRoutes);

// Global Error Handler
app.use((error, _req, res, _next) => {
  console.error('Unhandled Server Error:', error);
  res.status(500).json({ message: 'Internal Server Error' });
});

const PORT = process.env.PORT || 5050;

app.listen(PORT, () => {
  console.log(`🚀 API server listening on http://localhost:${PORT}`);
  if (process.env.MONGODB_URI) {
    connectDatabase()
      .then(() => console.log('✅ MongoDB connected successfully.'))
      .catch((error) => {
        console.warn(`⚠️ Database connection offline (${error.message}). Express API server running in standalone mode with file-backed persistence.`);
      });
  } else {
    console.log('ℹ️ Running in standalone Express mode with JSON file-backed persistence.');
  }
});
