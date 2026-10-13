import 'dotenv/config';
import express from 'express';
import cors from 'cors';
import morgan from 'morgan';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';
import mongoose from 'mongoose';
import { connectDatabase } from './config/db.js';
import authRoutes from './routes/authRoutes.js';
import courseRoutes from './routes/courseRoutes.js';
import eventRoutes from './routes/eventRoutes.js';
import analyticsRoutes from './routes/analyticsRoutes.js';
import authorRoutes from './routes/authorRoutes.js';
import syncRoutes from './routes/syncRoutes.js';
import attemptsRoutes from './routes/attemptsRoutes.js';
import authV2Routes from './routes/authRoutesV2.js';
import eventsV2Routes from './routes/eventsV2Routes.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();

// Allow all origins (localhost + deployed domains + file://)
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
  database: mongoose.connection.readyState === 1 ? 'connected' : 'offline',
  timestamp: new Date().toISOString()
}));

// Classic REST Routes
app.use('/api/auth', authRoutes);
app.use('/api/courses', courseRoutes);
app.use('/api/events', eventRoutes);
app.use('/api/analytics', analyticsRoutes);
app.use('/api/author', authorRoutes);

// V2 Full-State Sync, Real-Time Attempt & Telemetry Routes
app.use('/api/v2', syncRoutes);
app.use('/api/v2/attempts', attemptsRoutes);
app.use('/api/v2/auth', authV2Routes);
app.use('/api/v2/events', eventsV2Routes);

// Serve static frontend when deployed (Render / Railway / Docker / Monolith)
const clientDist = path.resolve(__dirname, '../../client/dist');
const clientPublic = path.resolve(__dirname, '../../client/public');
const docsPath = path.resolve(__dirname, '../../docs');

let staticDir = null;
if (fs.existsSync(clientDist)) staticDir = clientDist;
else if (fs.existsSync(docsPath)) staticDir = docsPath;
else if (fs.existsSync(clientPublic)) staticDir = clientPublic;

if (staticDir) {
  app.use(express.static(staticDir));
  app.get('*', (req, res, next) => {
    if (req.path.startsWith('/api')) return next();
    const indexPath = path.join(staticDir, 'index.html');
    if (fs.existsSync(indexPath)) {
      return res.sendFile(indexPath);
    }
    const studioPath = path.join(staticDir, 'Learning_Companion_Studio.html');
    if (fs.existsSync(studioPath)) {
      return res.sendFile(studioPath);
    }
    next();
  });
}

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
