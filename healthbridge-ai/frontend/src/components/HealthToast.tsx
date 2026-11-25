import { createContext,useCallback,useContext,useEffect,useState } from 'react';
import type { ReactNode } from 'react';
import { CheckCircle2,Info,TriangleAlert,X } from 'lucide-react';
import { getHealthBridgeLanguage,SAFE_TOAST_COPY } from '../content/healthbridgeCopy';
import type { SafeToastPreset } from '../content/healthbridgeCopy';
import { useTranslation } from 'react-i18next';

type Notice={id:number;preset:SafeToastPreset};
type ToastContextValue={notify:(preset:SafeToastPreset)=>void};
const ToastContext=createContext<ToastContextValue>({notify:()=>{}});
const trayLabels={en:'Notifications',ta:'அறிவிப்புகள்',hi:'सूचनाएँ',te:'నోటిఫికేషన్‌లు',ml:'അറിയിപ്പുകൾ',kn:'ಅಧಿಸೂಚನೆಗಳು',mr:'सूचना',bn:'বিজ্ঞপ্তি'};
const dismissLabels={en:'Dismiss notification',ta:'அறிவிப்பை மூடு',hi:'सूचना बंद करें',te:'నోటిఫికేషన్‌ను మూసివేయండి',ml:'അറിയിപ്പ് അടയ്ക്കുക',kn:'ಅಧಿಸೂಚನೆಯನ್ನು ಮುಚ್ಚಿ',mr:'सूचना बंद करा',bn:'বিজ্ঞপ্তি বন্ধ করুন'};

export function HealthToastProvider({children}:{children:ReactNode}){
  const [notices,setNotices]=useState<Notice[]>([]);
  const notify=useCallback((preset:SafeToastPreset)=>setNotices(current=>[...current,{id:Date.now()+Math.random(),preset}].slice(-4)),[]);
  const dismiss=useCallback((id:number)=>setNotices(current=>current.filter(item=>item.id!==id)),[]);
  const dismissAll=useCallback(()=>setNotices([]),[]);
  return <ToastContext.Provider value={{notify}}>{children}<DotMatrixToaster notices={notices} dismiss={dismiss} dismissAll={dismissAll}/></ToastContext.Provider>;
}

export function useHealthToast(){return useContext(ToastContext);}

function DotMatrixToaster({notices,dismiss,dismissAll}:{notices:Notice[];dismiss:(id:number)=>void;dismissAll:()=>void}){
  const {i18n}=useTranslation();
  const lang=getHealthBridgeLanguage(i18n.language);
  useEffect(()=>{
    if(!notices.length)return;
    const onKeyDown=(event:KeyboardEvent)=>{if(event.key==='Escape')dismissAll();};
    window.addEventListener('keydown',onKeyDown);
    return ()=>window.removeEventListener('keydown',onKeyDown);
  },[notices.length,dismissAll]);
  if(!notices.length)return null;
  return <aside className="hb-toast-tray" aria-label={trayLabels[lang]}>
    {notices.map(({id,preset})=><ToastCard key={id} id={id} preset={preset} lang={lang} closeLabel={dismissLabels[lang]} dismiss={dismiss}/>)}
  </aside>;
}

function ToastCard({id,preset,lang,closeLabel,dismiss}:{id:number;preset:SafeToastPreset;lang:ReturnType<typeof getHealthBridgeLanguage>;closeLabel:string;dismiss:(id:number)=>void}){
  const notice=SAFE_TOAST_COPY[lang][preset];
  useEffect(()=>{
    if(notice.duration===0)return;
    const timer=window.setTimeout(()=>dismiss(id),notice.duration??6500);
    return ()=>window.clearTimeout(timer);
  },[dismiss,id,notice.duration]);
  const Icon=notice.tone==='success'?CheckCircle2:notice.tone==='error'?TriangleAlert:Info;
  return <article className={`hb-toast hb-toast-${notice.tone}`} role={notice.tone==='error'?'alert':'status'} aria-live={notice.tone==='error'?'assertive':'polite'}>
    <span className="hb-toast-mark" aria-hidden="true"><span className="hb-dot-matrix"/><Icon size={17}/></span>
    <span className="hb-toast-copy"><strong>{notice.title}</strong><span>{notice.body}</span></span>
    <button type="button" className="hb-toast-close" onClick={()=>dismiss(id)} aria-label={closeLabel}><X size={16}/></button>
  </article>;
}
