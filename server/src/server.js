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

const app = express();
app.use(cors({ origin: process.env.CLIENT_URL, credentials: true }));
app.use(express.json({ limit: '100kb' }));
app.use(morgan('dev'));
app.get('/api/health', (_req, res) => res.json({ status: 'ok' }));
app.use('/api/auth', authRoutes); app.use('/api/courses', courseRoutes); app.use('/api/events', eventRoutes); app.use('/api/analytics', analyticsRoutes); app.use('/api/author', authorRoutes);
app.use((error, _req, res, _next) => { console.error(error); res.status(500).json({ message: 'Something went wrong.' }); });
connectDatabase().then(() => app.listen(process.env.PORT || 5050, () => console.log('API listening'))).catch((error) => { console.error('Database connection failed:', error.message); process.exit(1); });
