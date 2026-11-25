import { useTranslation } from 'react-i18next';
import { Activity,ArrowDownToLine,ArrowRight,CalendarDays,FileHeart,HeartHandshake,Hospital,MessageCircle,Users,WandSparkles } from 'lucide-react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useHealthToast } from '../components/HealthToast';
import { DASHBOARD_COPY,SAFE_TOAST_COPY,getHealthBridgeLanguage } from '../content/healthbridgeCopy';
import type { DashboardTileKey,SafeToastPreset } from '../content/healthbridgeCopy';
import type { Role } from '../types';

type Tile={key:DashboardTileKey;to:string;titleKey:string;icon:typeof Hospital};
const roleTiles:Record<Role,Tile[]>={
  patient:[
    {key:'journey',to:'/journey',titleKey:'journey',icon:HeartHandshake},
    {key:'finder',to:'/hospitals',titleKey:'hospitals',icon:Hospital},
    {key:'appointments',to:'/appointments',titleKey:'appointments',icon:CalendarDays},
    {key:'community',to:'/community',titleKey:'community',icon:Users},
    {key:'assistant',to:'/assistant',titleKey:'assistant',icon:WandSparkles}
  ],
  doctor:[
    {key:'appointments',to:'/appointments',titleKey:'appointments',icon:CalendarDays},
    {key:'records',to:'/records',titleKey:'records',icon:FileHeart},
    {key:'journey',to:'/journey',titleKey:'referral',icon:HeartHandshake},
    {key:'assistant',to:'/assistant',titleKey:'assistant',icon:WandSparkles}
  ],
  hospital:[
    {key:'appointments',to:'/appointments',titleKey:'appointments',icon:CalendarDays},
    {key:'finder',to:'/hospitals',titleKey:'facilities',icon:Hospital},
    {key:'community',to:'/community',titleKey:'community',icon:Users}
  ],
  pharmacy:[
    {key:'workspace',to:'/admin',titleKey:'pharmacy',icon:Activity},
    {key:'journey',to:'/journey',titleKey:'journey',icon:HeartHandshake},
    {key:'community',to:'/community',titleKey:'community',icon:Users}
  ],
  admin:[
    {key:'workspace',to:'/admin',titleKey:'admin',icon:Activity},
    {key:'finder',to:'/hospitals',titleKey:'facilities',icon:Hospital},
    {key:'community',to:'/community',titleKey:'community',icon:Users}
  ]
};
const demoPresets:SafeToastPreset[]=['appointmentRequestReceived','secureMessageReceived','refillRequestReceived','requestFailed'];

export function GlassyDashboard(){
  const {user}=useAuth();
  const {i18n,t}=useTranslation();
  const {notify}=useHealthToast();
  if(!user)return null;
  const lang=getHealthBridgeLanguage(i18n.language);
  const copy=DASHBOARD_COPY[lang];
  const tiles=roleTiles[user.role]||roleTiles.patient;
  const titleFor=(tile:Tile)=>tile.titleKey==='facilities'?copy.directoryTitle:tile.titleKey==='referral'?copy.referralTitle:tile.titleKey==='pharmacy'?copy.pharmacyTitle:tile.titleKey==='admin'?copy.adminTitle:t(tile.titleKey);
  const exportOverview=()=>{
    const quote=(value:string)=>`"${value.replace(/"/g,'""')}"`;
    const rows=[copy.csvHeaders,...tiles.map(tile=>[titleFor(tile),copy.tiles[tile.key],tile.to])];
    const csv=rows.map(row=>row.map(quote).join(',')).join('\r\n');
    const blob=new Blob([`\uFEFF${csv}`],{type:'text/csv;charset=utf-8'});
    const url=URL.createObjectURL(blob);
    const link=document.createElement('a');
    link.href=url;
    link.download='healthbridge-safe-overview.csv';
    link.click();
    URL.revokeObjectURL(url);
  };
  return <div className="portal-page glassy-dashboard">
    <section className="glassy-dashboard-hero" aria-labelledby="dashboard-title">
      <div className="glassy-dashboard-orb glassy-orb-one" aria-hidden="true"/>
      <div className="glassy-dashboard-orb glassy-orb-two" aria-hidden="true"/>
      <div className="glassy-dashboard-copy">
        <div className="glassy-dashboard-eyebrow"><span className="pulse-dot"/>{copy.dashboardLabel} · {copy.roles[user.role]}</div>
        <h1 id="dashboard-title">{copy.welcome}</h1>
        <p>{copy.subtitle}</p>
        <div className="glassy-dashboard-badges"><span><span className="demo-badge-dot"/>{copy.demo}</span><span>{copy.privateLabel}</span></div>
      </div>
      <button className="button button-white glassy-export" type="button" onClick={exportOverview} title={copy.exportNote}>
        <ArrowDownToLine size={16}/>{copy.export}
      </button>
      <div className="glassy-hero-decoration" aria-hidden="true"><HeartHandshake size={102}/></div>
    </section>

    <p className="glassy-export-note">{copy.exportNote}</p>

    <section className="hb-dashboard-grid" aria-label={t('dashboard')}>
      {tiles.map((tile,index)=>{
        const Icon=tile.icon;
        return <Link className={`hb-dashboard-card hb-dashboard-card-${index%4}`} to={tile.to} key={`${tile.key}-${tile.to}`}>
          <span className="hb-dashboard-icon" aria-hidden="true"><Icon size={20}/></span>
          <span className="hb-dashboard-card-copy"><strong>{titleFor(tile)}</strong><span>{copy.tiles[tile.key]}</span></span>
          <span className="hb-dashboard-open">{copy.open}<ArrowRight size={14}/></span>
        </Link>;
      })}
    </section>

    <div className="glassy-dashboard-safety" role="note"><Activity size={16}/><p>{copy.safety}</p></div>

    <section className="hb-notification-demo" aria-label={copy.preview}>
      <details>
        <summary><MessageCircle size={16}/><span>{copy.preview}</span><span className="notification-demo-hint">{copy.previewHelp}</span></summary>
        <div className="hb-notification-examples">
          {demoPresets.map(preset=><button type="button" key={preset} className="button button-outline button-small" onClick={()=>notify(preset)}>{SAFE_TOAST_COPY[lang][preset].title}</button>)}
        </div>
      </details>
    </section>
  </div>;
}

export const Dashboard=GlassyDashboard;
