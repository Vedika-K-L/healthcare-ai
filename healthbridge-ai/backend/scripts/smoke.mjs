import 'dotenv/config';
import fs from 'node:fs/promises';
import path from 'node:path';
import mongoose from 'mongoose';
import { connectDatabase } from '../src/config/db.js';
import { Appointment,ConsentRecord,DoctorProfile,MedicalDocument,Notification,PatientProfile,Prescription,Referral,User } from '../src/models/index.js';

const base=process.env.API_URL||'http://127.0.0.1:4000/api';
const stamp=Date.now();
const patientEmail=`hb.smoke.patient.${stamp}@example.test`;
const doctorEmail=`hb.smoke.doctor.${stamp}@example.test`;
let patientId,doctorId,documentId;
const pass=(condition,message)=>{if(!condition)throw new Error(`FAIL: ${message}`);console.log(`PASS ${message}`);};
async function call(method,route,{token,body,form,expected=200}={}){const headers={};if(token)headers.Authorization=`Bearer ${token}`;if(body){headers['Content-Type']='application/json';}const response=await fetch(`${base}${route}`,{method,headers,body:form|| (body?JSON.stringify(body):undefined)});const type=response.headers.get('content-type')||'';let data=null;if(type.includes('application/json'))data=await response.json();if(response.status!==expected)throw new Error(`${method} ${route} expected ${expected}, got ${response.status}: ${data?.message||''}`);return {response,data};}
try{
  await connectDatabase();
  const health=(await fetch(`${base}/health`)).json();
  const healthData=await health;
  pass(healthData.data?.database==='connected','API reports live MongoDB connection');
  const unauthorized=await call('GET','/appointments',{expected:401});
  pass(unauthorized.data.success===false,'protected API rejects requests without a token');
  const patient=(await call('POST','/auth/register',{expected:201,body:{name:'Smoke Test Patient',email:patientEmail,password:'SmokePass!2026',role:'patient',language:'en',location:{country:'India',state:'Tamil Nadu',district:'Namakkal',city:'Namakkal'}}})).data.data;
  patientId=patient.user.id;
  pass(patient.user.role==='patient'&&Boolean(patient.token),'patient registration returns a role-bound JWT');
  const login=(await call('POST','/auth/login',{body:{email:patientEmail,password:'SmokePass!2026'}})).data.data;
  pass(login.user.id===patientId,'patient login accepts the stored password hash');
  const me=(await call('GET','/auth/me',{token:login.token})).data.data.user;
  pass(me.email===patientEmail,'authenticated profile endpoint returns the current user');
  const profile=(await call('PATCH','/patients/me',{token:login.token,body:{bloodGroup:'O+',familyMembers:[{name:'Smoke Family',relationship:'Sibling'}]}})).data.data.profile;
  pass(profile.bloodGroup==='O+'&&profile.familyMembers.length===1,'patient profile and family records persist');
  const hospitals=(await call('GET','/hospitals?city=Chennai&specialty=Cardiology')).data.data.items;
  pass(hospitals.length>0&&hospitals[0].demo,'hospital search returns seeded fictional records');
  const doctor=(await call('POST','/auth/register',{expected:201,body:{name:'Smoke Test Doctor',email:doctorEmail,password:'SmokePass!2026',role:'doctor',language:'en',specialty:'Cardiology',registrationNumber:'SMOKE-001',location:{country:'India',state:'Tamil Nadu',city:'Chennai'}}})).data.data;
  doctorId=doctor.user.id;
  pass(doctor.user.role==='doctor','doctor registration creates a doctor role account');
  const admin=(await call('POST','/auth/login',{body:{email:process.env.DEMO_ADMIN_EMAIL||'admin@healthbridge.demo',password:process.env.DEMO_ADMIN_PASSWORD||'HealthBridgeDemo!2026'}})).data.data;
  await call('PATCH',`/doctors/${doctorId}/verification`,{token:admin.token,body:{verified:true}});
  pass(true,'admin can verify a doctor profile');
  const listedDoctors=(await call('GET','/doctors',{token:login.token})).data.data.items;
  pass(listedDoctors.some(item=>String(item._id)===doctorId),'verified doctor appears in the care directory');
  const future=new Date(Date.now()+5*86400000);future.setHours(10,0,0,0);
  const appointment=(await call('POST','/appointments',{token:login.token,body:{hospitalId:hospitals[0]._id,doctorId,date:future.toISOString(),specialty:'Cardiology',reason:'Smoke test visit'},expected:201})).data.data.appointment;
  pass(appointment.demo===true,'appointment request is stored with its demo hospital reference');
  const form=new FormData();form.append('file',new Blob(['%PDF-1.4\nHealthBridge demo document\n%%EOF'],{type:'application/pdf'}),'smoke-report.pdf');form.append('category','report');form.append('description','Temporary smoke test document');
  const document=(await call('POST','/documents/upload',{token:login.token,form,expected:201})).data.data.document;
  documentId=document._id;
  pass(document.category==='report','PDF document uploads through the backend');
  const doctorDocs=(await call('GET','/documents',{token:doctor.token})).data.data.items;
  pass(!doctorDocs.some(item=>String(item._id)===documentId),'doctor cannot see a private record before patient consent to that record scope');
  const consent=(await call('POST','/consents',{token:login.token,body:{doctorId,scope:'all'},expected:201})).data.data.consent;
  pass(Boolean(consent._id),'patient can grant record sharing consent');
  const grantedDocs=(await call('GET','/documents',{token:doctor.token}));
  pass(grantedDocs.response.status===200,'doctor document list is available after patient-wide consent');
  const download=await fetch(`${base}/documents/${documentId}/download`,{headers:{Authorization:`Bearer ${doctor.token}`}});
  pass(download.status===200&&(download.headers.get('content-type')||'').includes('application/pdf'),'consented doctor can download the document');
  const confirmed=(await call('PATCH',`/appointments/${appointment._id}`,{token:doctor.token,body:{status:'confirmed'}})).data.data.appointment;
  pass(confirmed.status==='confirmed','assigned doctor can update an appointment');
  const prescription=(await call('POST','/prescriptions',{token:doctor.token,body:{patientId,appointmentId:appointment._id,items:[{medicine:'Demo medicine',dosage:'Sample only',frequency:'As directed'}],notes:'Fictional smoke-test record'},expected:201})).data.data.prescription;
  const patientPrescriptions=(await call('GET','/prescriptions',{token:login.token})).data.data.items;
  pass(patientPrescriptions.some(item=>String(item._id)===String(prescription._id)),'prescription persists and is visible to its patient');
  const referral=(await call('POST','/referrals',{token:login.token,body:{details:'Specialist review for a fictional demo patient',referringFacility:'Namakkal Primary Care Centre',specialty:'Cardiology',hospitalId:hospitals[0]._id,appointmentId:appointment._id},expected:201})).data.data.referral;
  pass(/^HB-\d{4}-[A-F0-9]+$/.test(referral.passportCode),'referral passport receives a unique tracking code');
  const reminders=(await call('POST','/notifications',{token:login.token,body:{title:'Demo follow-up',message:'A follow-up reminder for smoke testing',type:'follow-up'},expected:201})).data.data.notification;
  const camps=(await call('GET','/camps')).data.data.items;
  pass(Boolean(reminders._id)&&camps.length>0,'notifications and community camp data are served from MongoDB');
  const denied=await call('POST','/hospitals',{token:login.token,body:{name:'Unauthorized test hospital'},expected:403});
  pass(denied.data.success===false,'patient role cannot create hospital listings');
  await call('GET','/users',{token:admin.token});
  pass(true,'admin can read paginated user management data');
  console.log('\nHealthBridge API smoke checks passed.');
}catch(error){console.error(error);process.exitCode=1;}
finally{
  if(patientId){
    const files=await MedicalDocument.find({patient:patientId}).select('filename');
    const uploadDir=path.resolve(process.cwd(),process.env.UPLOAD_DIR||'uploads');
    await Promise.all(files.map(file=>fs.unlink(path.join(uploadDir,file.filename)).catch(()=>{})));
    await Promise.all([Appointment.deleteMany({patient:patientId}),MedicalDocument.deleteMany({patient:patientId}),Prescription.deleteMany({patient:patientId}),Referral.deleteMany({patient:patientId}),Notification.deleteMany({user:patientId}),ConsentRecord.deleteMany({patient:patientId}),PatientProfile.deleteMany({user:patientId}),User.deleteOne({_id:patientId})]);
  }
  if(doctorId){await Promise.all([Appointment.deleteMany({doctor:doctorId}),Prescription.deleteMany({doctor:doctorId}),ConsentRecord.deleteMany({grantee:doctorId}),DoctorProfile.deleteMany({user:doctorId}),User.deleteOne({_id:doctorId})]);}
  await mongoose.disconnect();
}
