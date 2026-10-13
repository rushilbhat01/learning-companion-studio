import mongoose from 'mongoose';
import bcrypt from 'bcryptjs';

const userSchema = new mongoose.Schema({
  customId: { type: String, index: true },
  name: { type: String, required: true, trim: true, maxlength: 120 },
  email: { type: String, required: true, unique: true, lowercase: true, trim: true },
  passwordHash: { type: String, required: true, select: false },
  role: { type: String, enum: ['companion', 'author', 'learner', 'admin'], default: 'companion' }
}, { timestamps: true });

userSchema.methods.verifyPassword = function (password) { 
  return bcrypt.compare(password, this.passwordHash); 
};

userSchema.statics.hashPassword = (password) => bcrypt.hash(password, 10);

export default mongoose.models.User || mongoose.model('User', userSchema);
