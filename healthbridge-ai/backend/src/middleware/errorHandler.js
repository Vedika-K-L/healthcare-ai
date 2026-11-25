import multer from 'multer';
import { ZodError } from 'zod';
import { fail } from '../utils/response.js';
export function notFound(req,res){return fail(res,404,`Route not found: ${req.method} ${req.path}`);}
export function errorHandler(error,req,res,next){if(res.headersSent)return next(error);if(error instanceof ZodError)return fail(res,400,'Please check the information and try again.',error.issues.map(i=>({field:i.path.join('.'),message:i.message})));if(error instanceof multer.MulterError)return fail(res,400,error.code==='LIMIT_FILE_SIZE'?'Files must be 10 MB or smaller.':'The uploaded file could not be accepted.');if(error.code===11000)return fail(res,409,'An account with this email already exists.');console.error(error);return fail(res,error.status||500,error.status?error.message:'Something went wrong. Please try again.');}
