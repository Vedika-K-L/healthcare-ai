import bcrypt from 'bcryptjs';
import { Appointment,ConsentRecord,DoctorProfile,HealthcareCamp,Hospital,MedicalDocument,Medicine,Notification,PatientProfile,Pharmacy,Prescription,Referral,User } from '../models/index.js';

export async function prepareDatabase(){
  const models=[User,PatientProfile,DoctorProfile,Hospital,Pharmacy,Appointment,MedicalDocument,Prescription,Referral,Medicine,Notification,HealthcareCamp,ConsentRecord];
  for(const Model of models){await Model.createCollection().catch(error=>{if(error.codeName!=='NamespaceExists'&&error.code!==48)throw error;});await Model.init();}
  const adminEmail=(process.env.DEMO_ADMIN_EMAIL||'admin@healthbridge.demo').toLowerCase();
  const adminPassword=process.env.DEMO_ADMIN_PASSWORD||'HealthBridgeDemo!2026';
  const hash=await bcrypt.hash(adminPassword,12);
  await User.updateOne({email:adminEmail},{$setOnInsert:{name:'HealthBridge Demo Admin',email:adminEmail,passwordHash:hash,role:'admin',language:'en',isVerified:true}},{upsert:true});
  const hospitalData=[
    {name:'Kaveri Specialty Centre',type:'Multispecialty hospital',address:'Trichy Road, Namakkal',city:'Namakkal',district:'Namakkal',state:'Tamil Nadu',specialties:['Cardiology','Internal medicine','Orthopedics'],facilities:['Diagnostics','Teleconsultation','24/7 emergency'],accessibility:['Wheelchair access','Tamil speaking desk'],consultationFee:450,rating:4.6,phone:'+91 4286 230 100',demo:true},
    {name:'Chennai Central Heart Institute',type:'Specialty hospital',address:'Anna Salai, Chennai',city:'Chennai',district:'Chennai',state:'Tamil Nadu',specialties:['Cardiology','Cardiac surgery','Vascular care'],facilities:['Cardiac ICU','Diagnostics','Patient lodging desk','Teleconsultation'],accessibility:['Wheelchair access','Tamil and English support'],consultationFee:850,rating:4.8,phone:'+91 44 4000 1100',demo:true},
    {name:'Apollo First Med',type:'Multispecialty hospital',address:'Poonamallee High Road, Chennai',city:'Chennai',district:'Chennai',state:'Tamil Nadu',specialties:['Cardiology','Neurology','Oncology','Orthopedics'],facilities:['Diagnostics','Emergency','Pharmacy'],accessibility:['Wheelchair access','Interpreter support'],consultationFee:1000,rating:4.7,phone:'+91 44 2820 3333',demo:true}
  ];
  for(const h of hospitalData)await Hospital.updateOne({name:h.name},{$setOnInsert:h},{upsert:true});
  const campData=[{name:'Namakkal Heart Health Day',description:'Demo community screening camp with blood pressure and heart health education.',location:'District Community Hall',city:'Namakkal',date:new Date(Date.now()+14*86400000),services:['Blood pressure screening','Doctor consultation','Health awareness'],organizer:'HealthBridge Community Partners',demo:true},{name:'Healthy Families Mobile Clinic',description:'Demo public health information and family wellness event.',location:'Rasipuram Community Centre',city:'Rasipuram',date:new Date(Date.now()+24*86400000),services:['General check-up','Nutrition advice','Scheme support desk'],organizer:'Tamil Nadu Community Health Network',demo:true}];
  for(const c of campData)await HealthcareCamp.updateOne({name:c.name},{$setOnInsert:c},{upsert:true});
  let pharmacy=await Pharmacy.findOne({name:'People’s Care Pharmacy'});if(!pharmacy)pharmacy=await Pharmacy.create({name:'People’s Care Pharmacy',address:'Main Road, Namakkal',city:'Namakkal',phone:'+91 4286 220 501',demo:true,inventory:[{medicine:'Paracetamol 500 mg',quantity:42,price:18},{medicine:'ORS sachet',quantity:25,price:22}]});
  for(const m of [{name:'Paracetamol 500 mg',genericName:'Paracetamol',category:'Pain relief',price:18,available:true,pharmacy:pharmacy._id,demo:true},{name:'ORS sachet',genericName:'Oral rehydration salts',category:'Wellness',price:22,available:true,pharmacy:pharmacy._id,demo:true}])await Medicine.updateOne({name:m.name,pharmacy:m.pharmacy},{$setOnInsert:m},{upsert:true});
}
