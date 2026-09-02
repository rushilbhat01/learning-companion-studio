import mongoose from 'mongoose';

const quizAttemptSchema = new mongoose.Schema(
  {
    userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
    courseId: { type: mongoose.Schema.Types.ObjectId, ref: 'Course', required: true },
    lessonId: { type: mongoose.Schema.Types.ObjectId, required: true },
    score: { type: Number, required: true },
    totalQuestions: { type: Number, required: true },
    answers: [
      {
        questionId: { type: String },
        selectedChoice: { type: Number },
        isCorrect: { type: Boolean }
      }
    ]
  },
  { timestamps: true }
);

export default mongoose.model('QuizAttempt', quizAttemptSchema);
