import jwt from 'jsonwebtoken';
import { User } from '../models/index.js';
import { fail } from '../utils/response.js';
export async function authenticate(req,res,next){try{const h=req.headers.authorization||'';const token=h.startsWith('Bearer ')?h.slice(7):null;if(!token)return fail(res,401,'Please sign in to continue.');const payload=jwt.verify(token,process.env.JWT_SECRET);const user=await User.findById(payload.sub);if(!user||!user.active)return fail(res,401,'This account is unavailable.');req.user=user;next();}catch{return fail(res,401,'Your session has expired. Please sign in again.');}}
export const allowRoles=(...roles)=>(req,res,next)=>roles.includes(req.user?.role)?next():fail(res,403,'You do not have access to this resource.');
