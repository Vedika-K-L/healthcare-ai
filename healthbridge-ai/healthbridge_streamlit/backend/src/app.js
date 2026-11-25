import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import rateLimit from 'express-rate-limit';
import authRoutes from './routes/authRoutes.js';
import apiRoutes from './routes/apiRoutes.js';
import { errorHandler,notFound } from './middleware/errorHandler.js';
import { fail } from './utils/response.js';

const app=express();
const origins=(process.env.CLIENT_ORIGIN||'http://localhost:5173').split(',').map(v=>v.trim());
app.disable('x-powered-by');
app.use(helmet({crossOriginResourcePolicy:{policy:'cross-origin'}}));
app.use(cors({origin:(origin,cb)=>!origin||origins.includes(origin)?cb(null,true):cb(new Error('Origin is not allowed by CORS.')),credentials:false}));
app.use(express.json({limit:'1mb'}));
app.use(express.urlencoded({extended:false,limit:'1mb'}));
app.get('/api/health',(req,res)=>res.json({success:true,data:{status:'ok',database:globalThis.dbReady?'connected':'disconnected'}}));
app.use('/api/auth',rateLimit({windowMs:15*60*1000,limit:100,standardHeaders:true,legacyHeaders:false}),authRoutes);
app.use('/api',apiRoutes);
app.use(notFound);app.use(errorHandler);
export default app;

