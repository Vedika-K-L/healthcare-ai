from __future__ import annotations

import csv
import io
from datetime import datetime, time, timedelta, timezone
from typing import Any
from zoneinfo import ZoneInfo

import streamlit as st

from healthbridge_streamlit.api_client import APIError, HealthBridgeAPI, configured_api_url
from healthbridge_streamlit.components.ui.human_heart import render_human_heart
from healthbridge_streamlit.copy import HOME_FEATURES, LANGUAGES, UI


st.set_page_config(
    page_title="HealthBridge AI",
    page_icon="💚",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_URL = configured_api_url(st.secrets)
USER_TIMEZONE = ZoneInfo("Asia/Kolkata")

APP_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
:root{--hb-navy:#102e4b;--hb-teal:#168e88;--hb-ink:#182e43;--hb-muted:#6e8191;--hb-line:#e5edf1;--hb-page:#f5f8fb}
html,body,[class*="css"]{font-family:'DM Sans',system-ui,sans-serif}
[data-testid="stAppViewContainer"]{background:var(--hb-page);color:var(--hb-ink)}
[data-testid="stHeader"]{background:rgba(245,248,251,.84)}
.main .block-container{max-width:1400px;padding-top:1.5rem;padding-bottom:3rem}
[data-testid="stSidebar"]{background:#fff;border-right:1px solid #e7edf0}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p{color:#617786}
h1,h2,h3{font-family:'Manrope','DM Sans',sans-serif;color:var(--hb-navy);letter-spacing:-.035em}
.hb-eyebrow{color:#5b7b8c;font-size:.68rem;font-weight:800;letter-spacing:.14em;text-transform:uppercase;margin:0 0 .6rem}
.hb-hero{padding:2.2rem 2.3rem;border-radius:24px;background:linear-gradient(115deg,#102e4b 0%,#14465d 55%,#167f7c 100%);color:#f3fbfa;box-shadow:0 20px 44px rgba(16,46,75,.18)}
.hb-hero h1{color:#fff;font-size:clamp(2.25rem,4vw,3.6rem);line-height:1.04;margin:.3rem 0 1rem}
.hb-hero p{color:#deebef;max-width:42rem;line-height:1.75}
.hb-pill{display:inline-flex;align-items:center;gap:.5rem;border:1px solid rgba(255,255,255,.24);background:rgba(255,255,255,.11);border-radius:999px;padding:.45rem .75rem;color:#f2fbfa;font-size:.75rem}
.hb-card{border:1px solid var(--hb-line);border-radius:17px;padding:1rem 1.1rem;background:rgba(255,255,255,.86);box-shadow:0 9px 26px rgba(17,49,71,.055);height:100%}
.hb-card h3{font-size:1.05rem;margin:.3rem 0 .5rem}.hb-card p{color:var(--hb-muted);font-size:.9rem;line-height:1.6}
.hb-note{border:1px solid rgba(22,142,136,.2);border-radius:12px;padding:.85rem 1rem;background:rgba(22,142,136,.07);color:#506d78;font-size:.84rem;line-height:1.6}
.hb-quiet{color:#718392;font-size:.78rem}
.stButton>button,.stDownloadButton>button{border-radius:10px;border:1px solid #cbdedc;font-weight:700;min-height:2.65rem;transition:transform .16s ease,box-shadow .16s ease,border-color .16s ease}
.stButton>button:hover,.stDownloadButton>button:hover{transform:translateY(-1px);border-color:#168e88;box-shadow:0 8px 18px rgba(22,142,136,.12)}
.stButton>button:focus-visible,.stDownloadButton>button:focus-visible,input:focus-visible,textarea:focus-visible{outline:3px solid #55bdb5!important;outline-offset:2px!important}
[data-testid="stMetric"]{border:1px solid var(--hb-line);border-radius:14px;padding:1rem;background:#fff}
@media(prefers-reduced-motion:reduce){*,*:before,*:after{scroll-behavior:auto!important;animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important}}
.hb-photo-band{display:grid;grid-template-columns:.8fr 1.2fr;align-items:center;gap:2.4rem;margin:4.3rem 0 2rem;padding:3.2rem 0;border-top:1px solid var(--hb-line)}
.hb-photo-intro h2{max-width:25rem;margin:.5rem 0;color:var(--hb-navy);font:700 clamp(1.8rem,3vw,2.6rem)/1.1 'Manrope',sans-serif;letter-spacing:-.05em}
.hb-photo-intro p{max-width:24rem;color:var(--hb-muted);line-height:1.8}
.hb-photo-credit{color:#8696a1;font-size:.72rem}
.hb-photo-gallery{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));align-items:center;gap:.8rem;perspective:900px}
.hb-photo-card{position:relative;display:block;isolation:isolate;overflow:hidden;height:250px;border-radius:15px;background:#dce9e8;box-shadow:0 12px 28px rgba(19,49,69,.13);transform:rotate(var(--tilt,0deg));transition:transform .4s ease,box-shadow .4s ease}
.hb-photo-card:nth-child(2){--tilt:2deg;transform:translateY(-13px) rotate(var(--tilt))}
.hb-photo-card:nth-child(1){--tilt:-3deg}.hb-photo-card:nth-child(3){--tilt:-2deg}
.hb-photo-card img{width:100%;height:100%;object-fit:cover;filter:saturate(.86);transition:transform .6s ease,filter .4s ease}
.hb-photo-card:after{position:absolute;inset:30% 0 0;z-index:0;content:"";background:linear-gradient(180deg,transparent,rgba(8,27,38,.82))}
.hb-photo-card:hover,.hb-photo-card:focus-visible{z-index:2;transform:translateY(-9px) rotate(0) scale(1.035);box-shadow:0 22px 40px rgba(19,49,69,.24);outline:3px solid #168e88;outline-offset:3px}
.hb-photo-card:hover img,.hb-photo-card:focus-visible img{transform:scale(1.08);filter:saturate(1.08)}
.hb-photo-caption{position:absolute;z-index:1;right:.65rem;bottom:.85rem;left:.75rem;color:#fff;font-weight:700;font-size:.78rem;line-height:1.35}
.hb-photo-caption small{display:block;margin-top:.3rem;font-size:.57rem;letter-spacing:.1em;opacity:.82}
@media(max-width:850px){.hb-photo-band{grid-template-columns:1fr;gap:.6rem;padding:2.5rem 0}.hb-photo-gallery{min-height:235px}.hb-photo-card{height:220px}}
@media(max-width:520px){.hb-photo-gallery{gap:.45rem;min-height:190px}.hb-photo-card{height:185px;border-radius:11px}.hb-photo-caption{left:.5rem;bottom:.55rem;font-size:.66rem}.hb-photo-caption small{font-size:.48rem}}
@media(prefers-reduced-motion:reduce){.hb-photo-card,.hb-photo-card img{transition:none}.hb-photo-card:hover,.hb-photo-card:focus-visible{transform:none}.hb-photo-card:hover img,.hb-photo-card:focus-visible img{transform:none}}
</style>
"""
st.markdown(APP_CSS, unsafe_allow_html=True)


def init_state() -> None:
    defaults = {"hb_token": None, "hb_user": None, "hb_language": "en", "hb_navigation": "Home", "hb_hospital_results": None, "hb_journey_result": None}
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_state()


def api(token: str | None = None) -> HealthBridgeAPI:
    return HealthBridgeAPI(API_URL, token if token is not None else st.session_state.get("hb_token"))


def copy() -> dict[str, str]:
    return UI.get(st.session_state.get("hb_language", "en"), UI["en"])


def safe_notice(key: str) -> None:
    language = st.session_state.get("hb_language", "en")
    notices = {
        "en": {"request": ("Request received", "Your appointment request was received. Sign in to view its status."), "message": ("New secure message", "You have a new message in your patient portal. Sign in to view it."), "refill": ("Request submitted", "Your refill request was submitted. Sign in to check its status."), "record": ("Record saved", "Your document was saved to your private records."), "status": ("Status updated", "A request status was updated. Sign in to view private details."), "error": ("Request not submitted", "Please try again or contact the clinic for help.")},
        "ta": {"request": ("கோரிக்கை பெறப்பட்டது", "உங்கள் சந்திப்பு கோரிக்கை பெறப்பட்டது. அதன் நிலையைப் பார்க்க உள்நுழையவும்."), "message": ("புதிய பாதுகாப்பான செய்தி", "உங்கள் நோயாளர் போர்ட்டலில் புதிய செய்தி உள்ளது. அதைப் பார்க்க உள்நுழையவும்."), "refill": ("கோரிக்கை சமர்ப்பிக்கப்பட்டது", "மீண்டும் மருந்து பெறும் கோரிக்கை சமர்ப்பிக்கப்பட்டது. அதன் நிலையைப் பார்க்க உள்நுழையவும்."), "record": ("பதிவு சேமிக்கப்பட்டது", "உங்கள் ஆவணம் தனிப்பட்ட பதிவுகளில் சேமிக்கப்பட்டது."), "status": ("நிலை புதுப்பிக்கப்பட்டது", "ஒரு கோரிக்கையின் நிலை புதுப்பிக்கப்பட்டது. தனிப்பட்ட விவரங்களைப் பார்க்க உள்நுழையவும்."), "error": ("கோரிக்கை சமர்ப்பிக்கப்படவில்லை", "மீண்டும் முயற்சிக்கவும் அல்லது கிளினிக்கைத் தொடர்புகொள்ளவும்.")},
        "hi": {"request": ("अनुरोध प्राप्त हुआ", "आपका अपॉइंटमेंट अनुरोध प्राप्त हुआ। स्थिति देखने के लिए साइन इन करें."), "message": ("नया सुरक्षित संदेश", "आपके पेशेंट पोर्टल में नया संदेश है। देखने के लिए साइन इन करें."), "refill": ("अनुरोध भेजा गया", "दवा दोबारा लेने का अनुरोध भेजा गया। स्थिति देखने के लिए साइन इन करें."), "record": ("रिकॉर्ड सहेजा गया", "आपका दस्तावेज़ निजी रिकॉर्ड में सहेजा गया."), "status": ("स्थिति अपडेट हुई", "एक अनुरोध की स्थिति अपडेट हुई। निजी विवरण देखने के लिए साइन इन करें."), "error": ("अनुरोध नहीं भेजा गया", "फिर कोशिश करें या सहायता के लिए क्लिनिक से संपर्क करें.")},
        "te": {"request": ("అభ్యర్థన అందింది", "మీ అపాయింట్‌మెంట్ అభ్యర్థన అందింది. స్థితిని చూడటానికి సైన్ ఇన్ చేయండి."), "message": ("కొత్త సురక్షిత సందేశం", "మీ పేషెంట్ పోర్టల్‌లో కొత్త సందేశం ఉంది. చూడటానికి సైన్ ఇన్ చేయండి."), "refill": ("అభ్యర్థన సమర్పించబడింది", "మీ రీఫిల్ అభ్యర్థన సమర్పించబడింది. స్థితిని చూడటానికి సైన్ ఇన్ చేయండి."), "record": ("రికార్డు సేవ్ చేయబడింది", "మీ పత్రం మీ ప్రైవేట్ రికార్డుల్లో సేవ్ చేయబడింది."), "status": ("స్థితి నవీకరించబడింది", "అభ్యర్థన స్థితి నవీకరించబడింది. వ్యక్తిగత వివరాలను చూడటానికి సైన్ ఇన్ చేయండి."), "error": ("అభ్యర్థన సమర్పించబడలేదు", "మళ్లీ ప్రయత్నించండి లేదా సహాయం కోసం క్లినిక్‌ను సంప్రదించండి.")},
        "ml": {"request": ("അഭ്യർത്ഥന ലഭിച്ചു", "നിങ്ങളുടെ അപ്പോയിന്റ്മെന്റ് അഭ്യർത്ഥന ലഭിച്ചു. നില കാണാൻ സൈൻ ഇൻ ചെയ്യുക."), "message": ("പുതിയ സുരക്ഷിത സന്ദേശം", "നിങ്ങളുടെ രോഗി പോർട്ടലിൽ പുതിയ സന്ദേശമുണ്ട്. കാണാൻ സൈൻ ഇൻ ചെയ്യുക."), "refill": ("അഭ്യർത്ഥന സമർപ്പിച്ചു", "റീഫിൽ അഭ്യർത്ഥന സമർപ്പിച്ചു. നില പരിശോധിക്കാൻ സൈൻ ഇൻ ചെയ്യുക."), "record": ("രേഖ സംരക്ഷിച്ചു", "നിങ്ങളുടെ ഡോക്യുമെന്റ് സ്വകാര്യ രേഖകളിൽ സംരക്ഷിച്ചു."), "status": ("നില പുതുക്കി", "ഒരു അഭ്യർത്ഥനയുടെ നില പുതുക്കി. സ്വകാര്യ വിവരങ്ങൾ കാണാൻ സൈൻ ഇൻ ചെയ്യുക."), "error": ("അഭ്യർത്ഥന സമർപ്പിച്ചില്ല", "വീണ്ടും ശ്രമിക്കുക അല്ലെങ്കിൽ സഹായത്തിന് ക്ലിനിക്കുമായി ബന്ധപ്പെടുക.")},
        "kn": {"request": ("ವಿನಂತಿ ಸ್ವೀಕರಿಸಲಾಗಿದೆ", "ನಿಮ್ಮ ಅಪಾಯಿಂಟ್‌ಮೆಂಟ್ ವಿನಂತಿ ಸ್ವೀಕರಿಸಲಾಗಿದೆ. ಸ್ಥಿತಿ ನೋಡಲು ಸೈನ್ ಇನ್ ಮಾಡಿ."), "message": ("ಹೊಸ ಸುರಕ್ಷಿತ ಸಂದೇಶ", "ನಿಮ್ಮ ರೋಗಿ ಪೋರ್ಟಲ್‌ನಲ್ಲಿ ಹೊಸ ಸಂದೇಶವಿದೆ. ನೋಡಲು ಸೈನ್ ಇನ್ ಮಾಡಿ."), "refill": ("ವಿನಂತಿ ಸಲ್ಲಿಸಲಾಗಿದೆ", "ನಿಮ್ಮ ರೀಫಿಲ್ ವಿನಂತಿ ಸಲ್ಲಿಸಲಾಗಿದೆ. ಸ್ಥಿತಿ ಪರಿಶೀಲಿಸಲು ಸೈನ್ ಇನ್ ಮಾಡಿ."), "record": ("ದಾಖಲೆ ಉಳಿಸಲಾಗಿದೆ", "ನಿಮ್ಮ ದಾಖಲೆ ಖಾಸಗಿ ಆರೋಗ್ಯ ದಾಖಲೆಗಳಲ್ಲಿ ಉಳಿಸಲಾಗಿದೆ."), "status": ("ಸ್ಥಿತಿ ನವೀಕರಿಸಲಾಗಿದೆ", "ವಿನಂತಿಯ ಸ್ಥಿತಿ ನವೀಕರಿಸಲಾಗಿದೆ. ಖಾಸಗಿ ವಿವರಗಳನ್ನು ನೋಡಲು ಸೈನ್ ಇನ್ ಮಾಡಿ."), "error": ("ವಿನಂತಿ ಸಲ್ಲಿಸಲಾಗಿಲ್ಲ", "ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ ಅಥವಾ ಸಹಾಯಕ್ಕಾಗಿ ಕ್ಲಿನಿಕ್ ಸಂಪರ್ಕಿಸಿ.")},
        "mr": {"request": ("विनंती मिळाली", "तुमची अपॉइंटमेंट विनंती मिळाली. स्थिती पाहण्यासाठी साइन इन करा."), "message": ("नवीन सुरक्षित संदेश", "तुमच्या पेशंट पोर्टलमध्ये नवीन संदेश आहे. पाहण्यासाठी साइन इन करा."), "refill": ("विनंती पाठवली", "औषध पुन्हा मिळवण्याची विनंती पाठवली. स्थिती पाहण्यासाठी साइन इन करा."), "record": ("नोंद जतन केली", "तुमचा दस्तऐवज खाजगी नोंदींमध्ये जतन केला."), "status": ("स्थिती अद्ययावत केली", "विनंतीची स्थिती अद्ययावत केली. खाजगी तपशील पाहण्यासाठी साइन इन करा."), "error": ("विनंती पाठवली नाही", "पुन्हा प्रयत्न करा किंवा मदतीसाठी क्लिनिकशी संपर्क साधा.")},
        "bn": {"request": ("অনুরোধ পাওয়া গেছে", "আপনার অ্যাপয়েন্টমেন্টের অনুরোধ পাওয়া গেছে। অবস্থা দেখতে সাইন ইন করুন."), "message": ("নতুন নিরাপদ বার্তা", "আপনার রোগী পোর্টালে নতুন বার্তা আছে। দেখতে সাইন ইন করুন."), "refill": ("অনুরোধ জমা হয়েছে", "আপনার রিফিলের অনুরোধ জমা হয়েছে। অবস্থা দেখতে সাইন ইন করুন."), "record": ("নথি সংরক্ষিত", "আপনার নথি ব্যক্তিগত রেকর্ডে সংরক্ষিত হয়েছে."), "status": ("অবস্থা আপডেট হয়েছে", "একটি অনুরোধের অবস্থা আপডেট হয়েছে। ব্যক্তিগত বিবরণ দেখতে সাইন ইন করুন."), "error": ("অনুরোধ জমা হয়নি", "আবার চেষ্টা করুন অথবা সহায়তার জন্য ক্লিনিকে যোগাযোগ করুন.")},
    }
    title, body = notices.get(language, notices["en"]).get(key, notices["en"]["request"])
    st.toast(f"**{title}**\n\n{body}", icon="⚠️" if key == "error" else "💚")


def navigate(page: str) -> None:
    st.session_state["hb_navigation"] = page
    st.rerun()


def page_label(page: str, labels: dict[str, str]) -> str:
    keys = {"Home":"home", "Dashboard":"dashboard", "One Journey":"journey", "Find care":"hospitals", "Appointments":"appointments", "Medical records":"records", "AI assistant":"assistant", "Community care":"community", "My profile":"profile", "Administration":"admin", "Pharmacy workspace":"pharmacy", "Facility workspace":"admin", "Sign in":"sign_in", "Create account":"register"}
    return labels.get(keys.get(page, ""), page)


def get_items(client: HealthBridgeAPI, path: str, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    result = client.get(path, params=params or {})
    return result.get("items", []) if isinstance(result, dict) else []


def render_home(language: str, labels: dict[str, str]) -> None:
    left, right = st.columns([1.05, .95], gap="large", vertical_alignment="center")
    with left:
        st.markdown('<p class="hb-eyebrow">CARE, CONNECTED ACROSS DISTANCES</p>', unsafe_allow_html=True)
        st.markdown(f'<div class="hb-hero"><h1>{labels["welcome"]}</h1><p>{labels["tagline"]}</p><span class="hb-pill">Private by design&nbsp; · &nbsp;Patient-led records&nbsp; · &nbsp;Demo platform</span></div>', unsafe_allow_html=True)
        st.write("")
        a, b = st.columns(2)
        with a:
            if st.button(labels["register"], type="primary", use_container_width=True, key="home-register"):
                navigate("Create account")
        with b:
            if st.button(labels["sign_in"], use_container_width=True, key="home-login"):
                navigate("Sign in")
    with right:
        render_human_heart(420)
        st.caption("Anatomical heart illustration · showing the chambers and major vessels.")

    st.markdown("### Care coordination, made clearer")
    titles = [labels["hospitals"], labels["assistant"], labels["journey"], labels["community"]]
    destinations = ["Find care", "AI assistant", "One Journey", "Community care"]
    icons = ["🏥", "💬", "🧭", "🌿"]
    descriptions = HOME_FEATURES.get(language, HOME_FEATURES["en"])
    columns = st.columns(4, gap="small")
    for index, column in enumerate(columns):
        with column:
            st.markdown(f'<div class="hb-card"><div style="font-size:1.55rem">{icons[index]}</div><h3>{titles[index]}</h3><p>{descriptions[index]}</p></div>', unsafe_allow_html=True)
            if st.button(labels["open"], key=f"home-feature-{index}", use_container_width=True):
                navigate(destinations[index])
    st.markdown("""
    <section class="hb-photo-band" aria-label="Illustrative care photography">
      <div class="hb-photo-intro">
        <p class="hb-eyebrow">THE HUMAN SIDE OF CARE</p>
        <h2>Every care journey starts with a person.</h2>
        <p>Clear information works best alongside a little human support.</p>
        <span class="hb-photo-credit">Unsplash photography · shown for illustration</span>
      </div>
      <div class="hb-photo-gallery">
        <a class="hb-photo-card" href="https://unsplash.com/photos/a-doctor-showing-a-patient-something-on-the-tablet-J5UTvRgse7Q" target="_blank" rel="noopener noreferrer" aria-label="Unsplash photo: a doctor showing a patient information on a tablet">
          <img src="https://images.unsplash.com/photo-1666886573531-48d2e3c2b684?auto=format&amp;fit=crop&amp;w=900&amp;q=85" alt="A doctor showing a patient information on a tablet" loading="lazy">
          <span class="hb-photo-caption">Listening comes first<small>PEOPLE-FIRST CARE</small></span>
        </a>
        <a class="hb-photo-card" href="https://unsplash.com/s/photos/nurse-and-patient" target="_blank" rel="noopener noreferrer" aria-label="Unsplash photo: a nurse talking with an older patient">
          <img src="https://images.unsplash.com/photo-1576765608535-5f04d1e3f289?auto=format&amp;fit=crop&amp;w=900&amp;q=85" alt="A nurse talking with an older patient" loading="lazy">
          <span class="hb-photo-caption">Support along the way<small>CARE THAT CONNECTS</small></span>
        </a>
        <a class="hb-photo-card" href="https://unsplash.com/s/photos/doctor" target="_blank" rel="noopener noreferrer" aria-label="Unsplash photo: a healthcare professional ready to help">
          <img src="https://images.unsplash.com/photo-1622253692010-333f2da6031d?auto=format&amp;fit=crop&amp;w=900&amp;q=85" alt="A healthcare professional ready to help" loading="lazy">
          <span class="hb-photo-caption">Clarity at every step<small>YOUR NEXT STEP, MADE CLEAR</small></span>
        </a>
      </div>
    </section>
    """, unsafe_allow_html=True)
    st.markdown('<div class="hb-note">All facility details, fees, availability, camps, and example workflows are simulated. Confirm information directly with providers. HealthBridge AI does not diagnose or prescribe.</div>', unsafe_allow_html=True)


def render_login() -> None:
    labels = copy()
    st.markdown('<p class="hb-eyebrow">YOUR CARE SPACE</p>', unsafe_allow_html=True)
    st.title(labels["sign_in"])
    st.write(labels["login_help"])
    with st.form("hb-login"):
        email = st.text_input("Email address", autocomplete="email")
        password = st.text_input("Password", type="password", autocomplete="current-password")
        submitted = st.form_submit_button(labels["sign_in"], type="primary", use_container_width=True)
    if submitted:
        try:
            result = HealthBridgeAPI(API_URL).post("/auth/login", json={"email": email, "password": password})
            st.session_state["hb_token"] = result["token"]
            st.session_state["hb_user"] = result["user"]
            st.session_state["hb_language"] = result["user"].get("language", st.session_state["hb_language"])
            st.session_state["hb_navigation"] = "Dashboard"
            st.rerun()
        except (APIError, KeyError) as exc:
            st.error(str(exc) or "Sign in could not be completed.")
    with st.expander("Demo administrator access"):
        st.caption("Use the seeded local demo account from the README. Do not reuse demo credentials for real data.")


def render_register() -> None:
    st.markdown('<p class="hb-eyebrow">A BETTER CONNECTED CARE JOURNEY</p>', unsafe_allow_html=True)
    st.title(copy()["register"])
    with st.form("hb-register"):
        role = st.selectbox("Account type", ["patient", "doctor", "hospital", "pharmacy"], format_func=lambda value: {"patient":"Patient", "doctor":"Doctor", "hospital":"Hospital / Clinic", "pharmacy":"Pharmacy"}[value])
        name = st.text_input("Full name or contact name", max_chars=100)
        facility_name = st.text_input("Facility name", max_chars=150) if role in ("hospital", "pharmacy") else ""
        email = st.text_input("Email address", autocomplete="email")
        phone = st.text_input("Phone number (optional)", max_chars=24)
        password = st.text_input("Password", type="password", help="Use at least 8 characters.")
        specialty = st.text_input("Specialty", max_chars=100) if role == "doctor" else ""
        registration_number = st.text_input("Professional registration number", max_chars=100) if role == "doctor" else ""
        country, region, district, city = st.columns(4)
        country_value = country.text_input("Country", value="India")
        region_value = region.text_input("State", value="Tamil Nadu")
        district_value = district.text_input("District", value="Namakkal")
        city_value = city.text_input("City / town", value="Namakkal")
        submitted = st.form_submit_button("Create account", type="primary", use_container_width=True)
    if submitted:
        body = {"name":name,"email":email,"password":password,"phone":phone,"role":role,"language":st.session_state["hb_language"],"location":{"country":country_value,"state":region_value,"district":district_value,"city":city_value},"specialty":specialty,"registrationNumber":registration_number,"facilityName":facility_name}
        try:
            result = HealthBridgeAPI(API_URL).post("/auth/register", json=body)
            st.session_state["hb_token"] = result["token"]
            st.session_state["hb_user"] = result["user"]
            st.session_state["hb_navigation"] = "Dashboard"
            st.rerun()
        except (APIError, KeyError) as exc:
            st.error(str(exc) or "Account creation could not be completed.")
    st.caption("Provider verification is not implied by account creation. The AI assistant does not diagnose or prescribe.")


ROLE_TILES = {
    "patient": [("One Journey", "journey"), ("Find care", "hospitals"), ("Appointments", "appointments"), ("Community care", "community"), ("AI assistant", "assistant")],
    "doctor": [("Appointments", "appointments"), ("Medical records", "records"), ("One Journey", "journey"), ("AI assistant", "assistant")],
    "hospital": [("Appointments", "appointments"), ("Find care", "hospitals"), ("Community care", "community"), ("Facility workspace", "admin")],
    "pharmacy": [("Pharmacy workspace", "pharmacy"), ("One Journey", "journey"), ("Community care", "community")],
    "admin": [("Administration", "admin"), ("Find care", "hospitals"), ("Community care", "community")],
}


def render_notification_examples(language: str) -> None:
    labels = copy()
    with st.expander("Notification examples"):
        st.caption("Generic sample messages only. Toasts never contain private health details, appointment specifics, or clinical guidance.")
        samples = [("request", "Appointment request received"), ("message", "Secure message received"), ("refill", "Refill request submitted"), ("error", "Could not submit request")]
        columns = st.columns(2)
        for index, (key, button_label) in enumerate(samples):
            if columns[index % 2].button(button_label, key=f"toast-preview-{key}", use_container_width=True):
                safe_notice(key)


def render_dashboard(language: str, labels: dict[str, str], user: dict[str, Any]) -> None:
    role = user.get("role", "patient")
    st.markdown('<p class="hb-eyebrow">HEALTHBRIDGE AI · YOUR CARE SPACE</p>', unsafe_allow_html=True)
    left, right = st.columns([1.08, .92], gap="large", vertical_alignment="center")
    with left:
        st.markdown(f'<div class="hb-hero"><h1>{labels["dashboard"]}</h1><p>Choose a next step. Private details stay in their secure sections.</p><span class="hb-pill">{labels["demo"]} &nbsp;·&nbsp; Private to you</span></div>', unsafe_allow_html=True)
        st.caption("Dashboard cards and CSV exports contain only navigation information, not account or health details.")
        csv_buffer = io.StringIO()
        writer = csv.writer(csv_buffer)
        writer.writerow(["Section", "Page"])
        for page, _ in ROLE_TILES.get(role, ROLE_TILES["patient"]):
            writer.writerow([page_label(page, labels), page])
        st.download_button("Download safe overview (CSV)", csv_buffer.getvalue().encode("utf-8-sig"), "healthbridge-safe-overview.csv", "text/csv", key="safe-dashboard-csv")
    with right:
        render_human_heart(380)

    columns = st.columns(3, gap="small")
    for index, (page, description_key) in enumerate(ROLE_TILES.get(role, ROLE_TILES["patient"])):
        label = page_label(page, labels)
        safe_descriptions = {
            "One Journey":"Continue a guided care-coordination path. Demo progress is illustrative.",
            "Find care":"Explore sample facility listings. Confirm services and fees directly with providers.",
            "Appointments":"Open the secure appointment section to review private request details.",
            "Medical records":"Manage private records and sharing consent in the secure records area.",
            "Community care":"Explore sample community camps and public health resources.",
            "AI assistant":"Get help navigating services. The assistant does not diagnose or prescribe.",
            "Facility workspace":"Open the facility workspace. Listing details are not independently verified.",
            "Pharmacy workspace":"Manage sample medicine listings. This is not a live stock or prescription check.",
            "Administration":"Open platform management tools. Account details stay inside the secure workspace.",
        }
        with columns[index % 3]:
            st.markdown(f'<div class="hb-card"><h3>{label}</h3><p>{safe_descriptions.get(page, "Open this secure section for details.")}</p></div>', unsafe_allow_html=True)
            if st.button(labels.get("open", "Open section"), key=f"dash-{role}-{description_key}-{index}", use_container_width=True):
                navigate(page)
    st.markdown('<div class="hb-note">Hospital listings, availability, camps, and referral progress in this demo are simulated. Confirm information with providers. This dashboard does not provide medical advice.</div>', unsafe_allow_html=True)
    render_notification_examples(language)


def render_hospitals(client: HealthBridgeAPI, language: str, labels: dict[str, str], user: dict[str, Any]) -> None:
    st.markdown('<p class="hb-eyebrow">SMART HOSPITAL FINDER</p>', unsafe_allow_html=True)
    st.title("Find care that fits your needs")
    st.write("Compare sample services by location and specialty. Contact providers to confirm current details.")
    with st.form("hospital-search"):
        q_col, city_col, specialty_col = st.columns([1.3, 1, 1])
        q = q_col.text_input("Facility name", key="hospital-q")
        city = city_col.text_input("City or district", key="hospital-city")
        specialty = specialty_col.selectbox("Specialty", ["All specialties", "Cardiology", "Internal medicine", "Orthopedics", "Neurology", "Oncology"])
        submitted = st.form_submit_button(labels["search"], type="primary")
    if submitted or st.session_state.get("hb_hospital_results") is None:
        params = {"q":q,"city":city}
        if specialty != "All specialties":
            params["specialty"] = specialty
        try:
            st.session_state["hb_hospital_results"] = get_items(client, "/hospitals", params)
        except APIError as exc:
            st.error(str(exc))
    hospitals = st.session_state.get("hb_hospital_results") or []
    st.caption(f"{len(hospitals)} sample care options · Availability and fees are simulated.")
    columns = st.columns(2, gap="medium")
    for index, hospital in enumerate(hospitals):
        with columns[index % 2]:
            with st.container(border=True):
                st.subheader(hospital.get("name", "Healthcare facility"))
                st.caption(f"{hospital.get('city', 'Location to be confirmed')}, {hospital.get('state', 'India')} · {hospital.get('type', 'Care facility')}")
                st.write("**Specialties:** " + (", ".join(hospital.get("specialties") or []) or "Contact provider"))
                st.write(f"**Listed consultation fee:** ₹{hospital.get('consultationFee', '—')} · simulated")
                st.caption("Confirm services, fee, and availability directly with the facility.")
                if user.get("role") == "patient" and st.button("Select for appointment request", key=f"select-hospital-{hospital.get('_id')}"):
                    st.session_state["hb_selected_hospital"] = hospital.get("_id")
                    navigate("Appointments")
    if not hospitals:
        st.info(labels["empty"])


def render_appointments(client: HealthBridgeAPI, user: dict[str, Any]) -> None:
    st.markdown('<p class="hb-eyebrow">CARE COORDINATION</p>', unsafe_allow_html=True)
    st.title("Appointments")
    role = user.get("role")
    if role == "patient":
        try:
            hospitals = get_items(client, "/hospitals", {"limit":100})
        except APIError as exc:
            hospitals = []
            st.error(str(exc))
        if hospitals:
            hospital_ids = [str(h.get("_id")) for h in hospitals]
            names = {str(h.get("_id")): f"{h.get('name','Facility')} · {h.get('city','')}" for h in hospitals}
            default_id = st.session_state.get("hb_selected_hospital")
            default_ix = hospital_ids.index(default_id) if default_id in hospital_ids else 0
            with st.form("appointment-request"):
                selected_id = st.selectbox("Hospital or clinic", hospital_ids, index=default_ix, format_func=lambda value: names.get(value, value))
                specialty = st.text_input("Specialty", value="Cardiology")
                day, hour = st.columns(2)
                today = datetime.now(USER_TIMEZONE).date()
                preferred_day = day.date_input("Preferred date", value=today + timedelta(days=3), min_value=today)
                preferred_time = hour.time_input("Preferred time", value=time(10, 0))
                reason = st.text_area("Optional note", max_chars=1000, help="This note is kept in your secure appointment record.")
                submitted = st.form_submit_button("Request appointment", type="primary")
            if submitted:
                visit = datetime.combine(preferred_day, preferred_time, tzinfo=USER_TIMEZONE).astimezone(timezone.utc).isoformat()
                try:
                    client.post("/appointments", json={"hospitalId":selected_id,"date":visit,"specialty":specialty,"reason":reason})
                    safe_notice("request")
                    st.rerun()
                except APIError as exc:
                    st.error(str(exc))
        else:
            st.info("No facilities are available in this sample directory yet.")
    elif role not in ("doctor", "admin"):
        st.info("Appointment review is available to patient, doctor, and administrator accounts.")
    try:
        items = get_items(client, "/appointments", {"limit":100}) if role in ("patient", "doctor", "admin") else []
    except APIError as exc:
        st.error(str(exc))
        items = []
    st.subheader("Secure appointment details")
    if not items:
        st.info("When a request is created, its private details will appear here.")
    for item in items:
        hospital = item.get("hospital") or {}
        with st.container(border=True):
            date_text = item.get("date", "")
            try:
                date_text = datetime.fromisoformat(date_text.replace("Z", "+00:00")).astimezone(USER_TIMEZONE).strftime("%b %d, %Y · %I:%M %p")
            except (AttributeError, ValueError):
                pass
            st.markdown(f"**{hospital.get('name','Healthcare facility')}** · {date_text}")
            st.caption(f"{item.get('specialty') or 'Consultation'} · Status: {item.get('status','requested')}")
            if role in ("doctor", "admin") and item.get("patient"):
                st.caption(f"Patient: {item['patient'].get('name','Patient')}")
            if item.get("reason"):
                with st.expander("Private visit note"):
                    st.write(item["reason"])
            if role in ("doctor", "admin") and item.get("status") == "requested":
                status_col, action_col = st.columns([1, 1])
                next_status = status_col.selectbox(
                    "Update request status",
                    ["confirmed", "completed", "cancelled"],
                    index=0,
                    key=f"status-choice-{item.get('_id')}",
                )
                if action_col.button("Save status", key=f"confirm-appt-{item.get('_id')}"):
                    try:
                        client.patch(f"/appointments/{item['_id']}", json={"status":next_status})
                        safe_notice("status")
                        st.rerun()
                    except APIError as exc:
                        st.error(str(exc))


def render_journey(client: HealthBridgeAPI, user: dict[str, Any]) -> None:
    st.markdown('<p class="hb-eyebrow">HEALTHBRIDGE AI · ONE JOURNEY</p>', unsafe_allow_html=True)
    st.title("One care journey, connected")
    st.write("Plan a route from local care to a specialist facility. Listings, travel, and appointment availability are illustrative.")
    if user.get("role") != "patient":
        st.info("Referral passports are created from a patient account. Other roles can use their secure appointment workspace.")
        return
    try:
        hospitals = get_items(client, "/hospitals", {"city":"Chennai", "limit":50})
    except APIError as exc:
        hospitals = []
        st.error(str(exc))
    if not hospitals:
        st.info("No Chennai facilities match this sample directory yet. Try Find care to browse other locations.")
        return
    ids = [str(h.get("_id")) for h in hospitals]
    by_id = {str(h.get("_id")):h for h in hospitals}
    with st.form("one-journey-form"):
        specialty = st.selectbox("Specialty", ["Cardiology", "Neurology", "Orthopedics", "Oncology", "Internal medicine"])
        filtered = [h for h in hospitals if not h.get("specialties") or any(specialty.lower() in s.lower() for s in h.get("specialties", []))] or hospitals
        filtered_ids = [str(h.get("_id")) for h in filtered]
        selected_id = st.selectbox("Sample Chennai facility", filtered_ids, format_func=lambda value:f"{by_id[value].get('name','Facility')} · ₹{by_id[value].get('consultationFee','—')} demo fee")
        day_col, time_col = st.columns(2)
        today = datetime.now(USER_TIMEZONE).date()
        visit_day = day_col.date_input("Preferred visit date", value=today+timedelta(days=4), min_value=today)
        visit_time = time_col.time_input("Preferred time", value=time(10,0))
        details = st.text_area("What would you like the provider to know?", value="Specialist consultation and review", max_chars=1500)
        submitted = st.form_submit_button("Create appointment request and referral passport", type="primary")
    if submitted:
        selected = by_id[selected_id]
        try:
            appointment = client.post("/appointments", json={"hospitalId":selected_id,"date":datetime.combine(visit_day,visit_time,tzinfo=USER_TIMEZONE).astimezone(timezone.utc).isoformat(),"specialty":specialty,"reason":details}).get("appointment",{})
            referral = client.post("/referrals", json={"hospitalId":selected_id,"appointmentId":appointment.get("_id"),"referringFacility":"Namakkal Primary Care Centre","specialty":specialty,"details":details}).get("referral",{})
            st.session_state["hb_journey_result"] = {"appointment":appointment,"referral":referral,"hospital":selected,"specialty":specialty,"date":datetime.combine(visit_day,visit_time,tzinfo=USER_TIMEZONE),"details":details}
            safe_notice("request")
        except APIError as exc:
            st.error(str(exc))
    result = st.session_state.get("hb_journey_result")
    if result:
        referral = result["referral"]
        st.success("Your appointment request and referral passport were saved in your secure account.")
        with st.container(border=True):
            st.subheader("Digital Referral Passport · Demo")
            st.write(f"**Passport code:** {referral.get('passportCode','Created')}")
            st.write("**Route:** Namakkal → Chennai")
            st.write("**Status:** " + referral.get("status", "sent"))
            st.caption("Private visit details remain in your secure appointment and referral pages. Confirm the appointment directly with the facility.")
        pdf = build_referral_pdf({
            "patient": user.get("name", "HealthBridge patient"),
            "passport": referral.get("passportCode", "Created"),
            "facility": result["hospital"].get("name", "Chennai care facility"),
            "specialty": result.get("specialty", "Consultation"),
            "date": result.get("date").strftime("%d %b %Y, %I:%M %p %Z") if result.get("date") else "To be confirmed",
            "status": referral.get("status", "sent"),
            "details": result.get("details", "Specialist consultation and review"),
        })
        st.download_button("Download demo referral passport (PDF)", pdf, f"healthbridge-referral-{referral.get('passportCode','demo')}.pdf", "application/pdf", key="journey-referral-pdf")


def build_referral_pdf(fields: dict[str, str]) -> bytes:
    """Create a private, patient-controlled demo passport PDF."""
    from xml.sax.saxutils import escape

    from reportlab.lib import colors
    from reportlab.lib.enums import TA_LEFT
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import mm
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

    buffer = io.BytesIO()
    document = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=18 * mm, leftMargin=18 * mm, topMargin=18 * mm, bottomMargin=18 * mm)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="HBTitle", parent=styles["Title"], textColor=colors.HexColor("#102e4b"), alignment=TA_LEFT, fontName="Helvetica-Bold", fontSize=21, leading=26, spaceAfter=4 * mm))
    styles.add(ParagraphStyle(name="HBBody", parent=styles["BodyText"], textColor=colors.HexColor("#304c60"), fontName="Helvetica", fontSize=10, leading=15))
    rows = [[Paragraph(f"<b>{escape(label)}</b>", styles["HBBody"]), Paragraph(escape(str(value)), styles["HBBody"])] for label, value in [
        ("Patient", fields["patient"]),
        ("Passport code", fields["passport"]),
        ("Referring facility", "Namakkal Primary Care Centre"),
        ("Selected hospital", fields["facility"]),
        ("Specialty", fields["specialty"]),
        ("Appointment request", fields["date"]),
        ("Referral status", fields["status"]),
        ("Care note", fields["details"]),
    ]]
    table = Table(rows, colWidths=[43 * mm, 129 * mm], hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#edf5f5")),
        ("GRID", (0, 0), (-1, -1), .45, colors.HexColor("#dce7eb")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ]))
    story = [Paragraph("HEALTHBRIDGE AI", styles["HBTitle"]), Paragraph("Digital referral passport · Demo document", styles["HBBody"]), Spacer(1, 7 * mm), table, Spacer(1, 8 * mm), Paragraph("This sample document supports care coordination. Confirm appointments with the facility. It does not replace official referral paperwork or medical advice. Your records are not attached.", styles["HBBody"])]
    document.build(story)
    return buffer.getvalue()


def render_community(client: HealthBridgeAPI) -> None:
    st.markdown('<p class="hb-eyebrow">COMMUNITY CARE</p>', unsafe_allow_html=True)
    st.title("Community camps and resources")
    st.caption("Camp listings are sample information. Check dates and availability with the organizer.")
    try:
        camps = get_items(client, "/camps", {"limit":100})
    except APIError as exc:
        st.error(str(exc))
        camps = []
    if not camps:
        st.info("No community camps are listed in this sample dataset.")
    columns = st.columns(2, gap="medium")
    for index, camp in enumerate(camps):
        with columns[index % 2]:
            with st.container(border=True):
                st.subheader(camp.get("name", "Community camp"))
                st.caption(f"{camp.get('city','Location to be confirmed')} · {camp.get('date','Date to be confirmed')}")
                st.write(camp.get("description", "Sample community health resource."))
                if camp.get("services"):
                    st.write("**Services:** " + ", ".join(camp["services"]))
                st.caption("Sample listing · Contact the organizer to confirm details.")
    st.divider()
    st.subheader("Official public health resources")
    resource_a, resource_b = st.columns(2)
    resource_a.link_button("Ayushman Bharat PM-JAY", "https://beneficiary.nha.gov.in/", use_container_width=True)
    resource_b.link_button("myScheme government portal", "https://www.myscheme.gov.in/", use_container_width=True)
    st.caption("These links open official government websites. This demo does not assess eligibility or benefits.")


def render_assistant() -> None:
    st.markdown('<p class="hb-eyebrow">NAVIGATION ASSISTANT</p>', unsafe_allow_html=True)
    st.title("How can I help you find your next step?")
    st.write("This assistant helps navigate HealthBridge AI. It does not diagnose, recommend treatment, or prescribe medicines.")
    topics = {"Find a hospital":"Find care", "Plan a specialist journey":"One Journey", "Request or review an appointment":"Appointments", "Manage private records":"Medical records", "Explore community camps":"Community care", "Manage consent":"My profile"}
    chosen = st.selectbox("Choose a HealthBridge topic", list(topics))
    st.info(f"Open **{topics[chosen]}** from the navigation to continue. Your medical decisions remain with your care team.")
    if st.button("Open this section", type="primary", key="assistant-open-selected"):
        navigate(topics[chosen])
    columns = st.columns(3)
    for index, (question, destination) in enumerate(list(topics.items())[:3]):
        if columns[index].button(question, key=f"assistant-{index}"):
            navigate(destination)


def render_records(client: HealthBridgeAPI, user: dict[str, Any]) -> None:
    st.markdown('<p class="hb-eyebrow">PRIVATE HEALTH LIBRARY</p>', unsafe_allow_html=True)
    st.title("Medical records and consent")
    role = user.get("role")
    if role in ("patient", "doctor"):
        patient_ids: list[str] = []
        patient_names: dict[str, str] = {}
        if role == "doctor":
            try:
                patients = get_items(client, "/doctors/patients")
                patient_ids = [str(item.get("_id")) for item in patients]
                patient_names = {str(item.get("_id")): item.get("name", "Consenting patient") for item in patients}
            except APIError as exc:
                st.error(str(exc))
        st.subheader("Upload a private document")
        selected_patient = None
        if role == "doctor" and patient_ids:
            selected_patient = st.selectbox("Patient who granted record access", patient_ids, format_func=lambda value: patient_names.get(value, "Consenting patient"))
        elif role == "doctor":
            st.info("A patient must grant record access before you can upload on their behalf.")
        file = st.file_uploader("Choose a PDF, JPEG, PNG, or WebP file (up to 10 MB)", type=["pdf","jpg","jpeg","png","webp"], key="hb-record-upload")
        category = st.selectbox("Document type", ["report", "prescription", "imaging", "referral", "other"])
        description = st.text_input("Short private note (optional)", max_chars=500)
        if st.button("Save to private records", type="primary", disabled=file is None or (role == "doctor" and selected_patient is None), key="save-record") and file:
            try:
                form_data = {"category":category,"description":description}
                if selected_patient:
                    form_data["patientId"] = selected_patient
                client.post("/documents/upload", data=form_data, files={"file":(file.name,file.getvalue(),file.type or "application/octet-stream")})
                safe_notice("record")
                st.rerun()
            except APIError as exc:
                st.error(str(exc))
        st.caption("Files stay private. A doctor needs your consent to view them.")
    if role in ("patient", "doctor", "admin"):
        try:
            documents = get_items(client, "/documents")
        except APIError as exc:
            documents = []
            st.error(str(exc))
        st.subheader("Secure document library")
        if not documents:
            st.info("Documents available to this account will appear here.")
        for item in documents:
            with st.container(border=True):
                st.markdown(f"**{item.get('originalName','Health document')}** · {item.get('category','document')}")
                st.caption(f"Uploaded {str(item.get('createdAt',''))[:10]} · private record")
                if item.get("description"):
                    with st.expander("Private note"):
                        st.write(item["description"])
                try:
                    content, filename = client.download(f"/documents/{item['_id']}/download")
                    st.download_button("Download private document", content, filename, item.get("mimeType","application/octet-stream"), key=f"download-doc-{item['_id']}")
                except APIError as exc:
                    st.caption(str(exc))
    if role == "patient":
        st.divider()
        st.subheader("Share records with a doctor")
        try:
            doctors = get_items(client, "/doctors")
        except APIError as exc:
            doctors = []
            st.error(str(exc))
        if doctors:
            doctor_ids = [str(item.get("_id")) for item in doctors]
            by_id = {str(item.get("_id")):item for item in doctors}
            selected = st.selectbox("Verified doctor", doctor_ids, format_func=lambda value:f"{by_id[value].get('name','Doctor')} · {by_id[value].get('specialty','Specialty')}")
            st.caption("This grants patient-wide access. The choice can be reviewed through your care team.")
            if st.button("Grant record access", key="grant-consent"):
                try:
                    client.post("/consents", json={"doctorId":selected,"scope":"all"})
                    st.success("Record access was granted to the selected doctor.")
                except APIError as exc:
                    st.error(str(exc))
        else:
            st.info("No verified doctors are listed in the sample directory.")


def render_profile(client: HealthBridgeAPI, user: dict[str, Any], language: str) -> None:
    st.markdown('<p class="hb-eyebrow">ACCOUNT AND FAMILY CARE</p>', unsafe_allow_html=True)
    st.title("My profile")
    with st.form("account-settings"):
        name = st.text_input("Name", value=user.get("name", ""), max_chars=100)
        phone = st.text_input("Phone number", value=user.get("phone", ""), max_chars=24)
        language_code = st.selectbox("Interface language", list(LANGUAGES), index=list(LANGUAGES).index(language), format_func=lambda code:LANGUAGES[code])
        account_submit = st.form_submit_button("Save account settings")
    if account_submit:
        try:
            result = client.patch("/users/me", json={"name":name,"phone":phone,"language":language_code}).get("user")
            if result:
                st.session_state["hb_user"] = result
            st.session_state["hb_language"] = language_code
            safe_notice("status")
            st.rerun()
        except APIError as exc:
            st.error(str(exc))
    if user.get("role") != "patient":
        return
    try:
        profile = client.get("/patients/me").get("profile", {})
    except APIError as exc:
        st.error(str(exc))
        return
    st.divider()
    st.subheader("Private patient profile")
    with st.form("patient-profile"):
        blood = st.text_input("Blood group (optional)", value=profile.get("bloodGroup", ""), max_chars=5)
        gender = st.text_input("Gender (optional)", value=profile.get("gender", ""), max_chars=40)
        allergies = st.text_input("Allergies (optional, comma separated)", value=", ".join(profile.get("allergies", [])))
        conditions = st.text_input("Conditions (optional, comma separated)", value=", ".join(profile.get("conditions", [])))
        emergency = profile.get("emergencyContact") or {}
        ec1, ec2, ec3 = st.columns(3)
        ec_name = ec1.text_input("Emergency contact name", value=emergency.get("name", ""))
        ec_phone = ec2.text_input("Emergency contact phone", value=emergency.get("phone", ""))
        ec_relation = ec3.text_input("Relationship", value=emergency.get("relationship", ""))
        profile_submit = st.form_submit_button("Save private profile")
    if profile_submit:
        body = {"bloodGroup":blood,"gender":gender,"allergies":[v.strip() for v in allergies.split(",") if v.strip()],"conditions":[v.strip() for v in conditions.split(",") if v.strip()],"emergencyContact":{"name":ec_name,"phone":ec_phone,"relationship":ec_relation}}
        try:
            client.patch("/patients/me", json=body)
            st.success("Your private profile was saved.")
        except APIError as exc:
            st.error(str(exc))
    st.subheader("Family health guardian")
    members = profile.get("familyMembers", []) or []
    for member in members:
        st.caption(f"{member.get('name','Family member')} · {member.get('relationship','Family')}")
    with st.form("add-family-member"):
        member_name = st.text_input("Family member name")
        relationship = st.text_input("Relationship", value="Family member")
        add_member = st.form_submit_button("Add family member")
    if add_member:
        if len(member_name.strip()) < 2:
            st.error("Enter a name with at least two characters.")
        else:
            try:
                client.patch("/patients/me", json={"familyMembers":members+[ {"name":member_name.strip(),"relationship":relationship.strip() or "Family member"} ]})
                st.success("Family profile saved in your secure account.")
                st.rerun()
            except APIError as exc:
                st.error(str(exc))


def render_admin(client: HealthBridgeAPI) -> None:
    st.markdown('<p class="hb-eyebrow">PLATFORM MANAGEMENT</p>', unsafe_allow_html=True)
    st.title("Care network administration")
    try:
        users = get_items(client, "/users", {"limit":100})
        hospitals = get_items(client, "/hospitals", {"limit":100})
    except APIError as exc:
        st.error(str(exc))
        return
    columns = st.columns(3)
    columns[0].metric("Registered accounts", len(users))
    columns[1].metric("Hospital listings", len(hospitals))
    columns[2].metric("Provider accounts", sum(1 for item in users if item.get("role") in ("doctor","hospital","pharmacy")))
    st.caption("Administrative records are visible only in this authenticated admin workspace. Sample facility data is illustrative.")
    with st.expander("Add a hospital listing"):
        with st.form("admin-hospital-add"):
            name = st.text_input("Facility name")
            city = st.text_input("City")
            state = st.text_input("State", value="Tamil Nadu")
            specialties = st.text_input("Specialties (comma separated)")
            fee = st.number_input("Listed consultation fee (₹)", min_value=0.0, value=0.0, step=50.0)
            submitted = st.form_submit_button("Save facility")
        if submitted:
            try:
                client.post("/hospitals", json={"name":name,"city":city,"state":state,"specialties":[v.strip() for v in specialties.split(",") if v.strip()],"consultationFee":fee,"demo":True})
                st.success("The listing was saved. Confirm its details before presenting it as verified.")
                st.rerun()
            except APIError as exc:
                st.error(str(exc))
    st.subheader("Provider verification")
    for item in users:
        if item.get("role") == "doctor":
            with st.container(border=True):
                st.write(f"**{item.get('name','Doctor')}** · {item.get('email','')} · {'Verified' if item.get('isVerified') else 'Verification pending'}")
                if not item.get("isVerified") and st.button("Verify provider profile", key=f"verify-doctor-{item.get('id')}"):
                    try:
                        client.patch(f"/doctors/{item['id']}/verification", json={"verified":True})
                        st.success("Provider verification status updated.")
                        st.rerun()
                    except APIError as exc:
                        st.error(str(exc))
    try:
        pending = get_items(client, "/admin/hospitals/pending")
    except APIError:
        pending = []
    if pending:
        st.subheader("Pending facility listings")
        for item in pending:
            with st.container(border=True):
                st.write(f"**{item.get('name','Facility')}** · {item.get('city','')}")
                st.caption("Verify the submitted details with the provider before activating this listing.")
                if st.button("Activate listing", key=f"activate-hospital-{item.get('_id')}"):
                    try:
                        client.patch(f"/hospitals/{item['_id']}/verification", json={"active":True})
                        st.success("Facility listing activated.")
                        st.rerun()
                    except APIError as exc:
                        st.error(str(exc))
    with st.expander("Secure account directory"):
        for item in users:
            st.caption(f"{item.get('role','account').title()} · {item.get('name','Account')} · {item.get('email','')}")


def render_facility_workspace(client: HealthBridgeAPI, user: dict[str, Any]) -> None:
    st.markdown('<p class="hb-eyebrow">FACILITY WORKSPACE</p>', unsafe_allow_html=True)
    st.title("Facility listing workspace")
    st.info("Facility listings and appointment availability are not independently verified by this demo.")
    with st.form("facility-listing"):
        name = st.text_input("Facility name", value="")
        city = st.text_input("City", value=(user.get("location") or {}).get("city", ""))
        state = st.text_input("State", value=(user.get("location") or {}).get("state", "Tamil Nadu"))
        specialties = st.text_input("Specialties (comma separated)")
        submitted = st.form_submit_button("Submit facility listing", type="primary")
    if submitted:
        try:
            client.post("/hospitals", json={"name":name,"city":city,"state":state,"specialties":[s.strip() for s in specialties.split(",") if s.strip()]})
            st.success("Facility listing submitted. Confirm its details before relying on it.")
        except APIError as exc:
            st.error(str(exc))


def render_pharmacy(client: HealthBridgeAPI) -> None:
    st.markdown('<p class="hb-eyebrow">PHARMACY SERVICES</p>', unsafe_allow_html=True)
    st.title("Medicine listing workspace")
    st.warning("This demo does not connect to live pharmacy stock, prices, prescriptions, or orders.")
    with st.form("medicine-search"):
        query = st.text_input("Search sample medicine listings")
        searched = st.form_submit_button("Search")
    try:
        result = client.get("/medicines", params={"q":query if searched else ""})
        medicines = result.get("items", [])
    except APIError as exc:
        medicines = []
        st.error(str(exc))
    for medicine in medicines:
        with st.container(border=True):
            st.write(f"**{medicine.get('name','Medicine')}** · {medicine.get('genericName') or medicine.get('category') or 'Sample listing'}")
            st.caption("Availability and pricing are not live. Confirm directly with the pharmacy.")
    with st.expander("Add or update a sample listing"):
        with st.form("medicine-add"):
            name = st.text_input("Medicine name")
            generic = st.text_input("Generic name (optional)")
            category = st.text_input("Category (optional)")
            available = st.checkbox("Listed as available in this demo", value=True)
            submitted = st.form_submit_button("Save listing")
        if submitted:
            try:
                client.post("/medicines", json={"name":name,"genericName":generic,"category":category,"available":available})
                st.success("Sample listing saved. This does not verify real inventory.")
                st.rerun()
            except APIError as exc:
                st.error(str(exc))


def main() -> None:
    user = st.session_state.get("hb_user")
    initial_lang = (user or {}).get("language", st.session_state.get("hb_language", "en"))
    if initial_lang in LANGUAGES and st.session_state.get("hb_language") == "en" and initial_lang != "en":
        st.session_state["hb_language"] = initial_lang

    st.sidebar.markdown("### 💚 HealthBridge AI")
    language = st.sidebar.selectbox("Language / மொழி", list(LANGUAGES), format_func=lambda code:LANGUAGES[code], key="hb_language")
    labels = UI.get(language, UI["en"])
    user = st.session_state.get("hb_user")
    if user:
        st.sidebar.caption(f"{user.get('role','account').title()} workspace · secure session")
        pages = ["Dashboard", "One Journey", "Find care", "Appointments", "Medical records", "AI assistant", "Community care", "My profile"]
        if user.get("role") == "admin":
            pages.append("Administration")
        elif user.get("role") == "pharmacy":
            pages.append("Pharmacy workspace")
        elif user.get("role") == "hospital":
            pages.append("Facility workspace")
        pages.append("Sign out")
    else:
        pages = ["Home", "Sign in", "Create account"]
    if st.session_state.get("hb_navigation") not in pages:
        st.session_state["hb_navigation"] = pages[0]
    if st.session_state.get("hb_navigation_picker") != st.session_state["hb_navigation"]:
        st.session_state["hb_navigation_picker"] = st.session_state["hb_navigation"]
    page = st.sidebar.radio(
        "Navigate",
        pages,
        key="hb_navigation_picker",
        format_func=lambda value:page_label(value, labels),
        on_change=lambda: st.session_state.update(hb_navigation=st.session_state["hb_navigation_picker"]),
    )
    st.session_state["hb_navigation"] = page
    try:
        health = HealthBridgeAPI(API_URL).health()
        st.sidebar.success("API connected · " + str(health.get("database", "ready")))
    except APIError:
        st.sidebar.caption("API disconnected · set HEALTHBRIDGE_API_URL to your deployed backend")
    if user and st.sidebar.button(labels["sign_out"], use_container_width=True):
        try:
            api().post("/auth/logout")
        except APIError:
            pass
        for key in ("hb_user", "hb_token", "hb_journey_result", "hb_hospital_results"):
            st.session_state.pop(key, None)
        st.session_state["hb_navigation"] = "Home"
        st.rerun()

    if page == "Home":
        render_home(language, labels)
    elif page == "Sign in":
        render_login()
    elif page == "Create account":
        render_register()
    elif not user:
        render_login()
    else:
        client = api()
        if page == "Dashboard":
            render_dashboard(language, labels, user)
        elif page == "One Journey":
            render_journey(client, user)
        elif page == "Find care":
            render_hospitals(client, language, labels, user)
        elif page == "Appointments":
            render_appointments(client, user)
        elif page == "Medical records":
            render_records(client, user)
        elif page == "AI assistant":
            render_assistant()
        elif page == "Community care":
            render_community(client)
        elif page == "My profile":
            render_profile(client, user, language)
        elif page == "Administration" and user.get("role") == "admin":
            render_admin(client)
        elif page == "Pharmacy workspace" and user.get("role") == "pharmacy":
            render_pharmacy(client)
        elif page == "Facility workspace" and user.get("role") == "hospital":
            render_facility_workspace(client, user)
        else:
            render_dashboard(language, labels, user)
    st.markdown("<hr><span class='hb-quiet'>HealthBridge AI · Demo platform · Your health information is yours to control.</span>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
