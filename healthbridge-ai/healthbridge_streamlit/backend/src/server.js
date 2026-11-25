import 'dotenv/config';
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import app from './app.js';
import { connectDatabase } from './config/db.js';
import { prepareDatabase } from './services/seedService.js';

const here=path.dirname(fileURLToPath(import.meta.url));
const uploadDir=path.resolve(here,'..',process.env.UPLOAD_DIR||'uploads');
process.env.UPLOAD_DIR=uploadDir;
await fs.mkdir(uploadDir,{recursive:true});
try{
  await connectDatabase();
  await prepareDatabase();
  globalThis.dbReady=true;
  const port=Number(process.env.PORT||4000);
  app.listen(port,'0.0.0.0',()=>console.log(`HealthBridge API listening at http://localhost:${port}`));
}catch(error){console.error('Backend startup failed:',error.message);process.exit(1);}
