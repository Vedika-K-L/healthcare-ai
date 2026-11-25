export type Role = 'patient'|'doctor'|'hospital'|'pharmacy'|'admin';
export interface User { id:string; name:string; email:string; phone?:string; role:Role; language:string; location?:{country?:string;state?:string;district?:string;city?:string}; isVerified:boolean }
export interface Hospital { _id:string; name:string; type:string; address:string; city:string; district?:string; state:string; specialties:string[]; facilities:string[]; accessibility:string[]; consultationFee:number; rating:number; phone:string; demo:boolean }
