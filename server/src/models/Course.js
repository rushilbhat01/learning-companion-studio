import mongoose from 'mongoose';

const lessonSchema = new mongoose.Schema({
  title: { type: String, required: true },
  summary: String,
  content: { type: String, required: true },
  videoUrl: String,
  durationMinutes: { type: Number, default: 10 },
  order: { type: Number, required: true },
  // LCM Pedagogical Fields
  led: {
    videoUrl: String,
    transcript: String,
    reflectionSpots: [{
      timestampSeconds: { type: Number, default: 45 },
      prompt: String,
      spotType: { type: String, default: 'reflection' } // 'reflection' | 'mcq' | 'subjective'
    }]
  },
  lbd: {
    mcqs: [{
      question: String,
      choices: [String],
      correctIndex: Number,
      feedbacks: [String]
    }],
    subjectives: [{
      prompt: String,
      exemplarAnswer: String
    }]
  },
  lxt: [{
    title: String,
    url: String,
    summary: String,
    extraType: { type: String, default: 'video' } // 'video' | 'link' | 'practice'
  }],
  lxi: {
    question: String
  }
}, { _id: true });

const courseSchema = new mongoose.Schema({
  title: { type: String, required: true },
  description: String,
  category: String,
  level: { type: String, default: 'Beginner' },
  accent: { type: String, default: 'blue' },
  lessons: [lessonSchema],
  quizzes: [{ lessonId: mongoose.Schema.Types.ObjectId, questions: [{ prompt: String, options: [String], answer: Number }] }]
}, { timestamps: true });
export default mongoose.model('Course', courseSchema);
