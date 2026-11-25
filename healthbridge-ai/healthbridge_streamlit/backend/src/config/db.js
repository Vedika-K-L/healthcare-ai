import mongoose from 'mongoose';
export async function connectDatabase(uri = process.env.MONGODB_URI) {
  if (!uri) throw new Error('MONGODB_URI is required. Copy .env.example to .env and configure MongoDB.');
  mongoose.set('strictQuery', true);
  await mongoose.connect(uri, { serverSelectionTimeoutMS: 6000 });
  console.log(`MongoDB connected: ${mongoose.connection.name}`);
  return mongoose.connection;
}
