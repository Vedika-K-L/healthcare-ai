# HEALTHBRIDGE AI

**From Your Village to the Right Healthcare Service.**

HealthBridge AI is a full-stack healthcare coordination demo with a **Streamlit frontend**, an Express REST API, and MongoDB persistence. The main end-to-end demonstration plans a patient journey from Namakkal to specialist care in Chennai. The previous React + TypeScript frontend remains in `frontend/` as an optional reference; Streamlit is the hosted entry point.

All hospitals, fees, pharmacies, availability, community events, and sample medical information supplied by the demo are fictional. The assistant provides navigation help only. It does not diagnose, recommend treatment, or prescribe medicines.

## Run the Streamlit frontend

The Streamlit app calls the existing Express API from the Python server. Streamlit hosts the frontend; the API and MongoDB still need to run locally or be deployed as separate services.

Requirements: Python 3.10 or newer, Node.js 20 or newer, npm, and MongoDB (local or hosted).

From this directory, create a Python environment and install the frontend dependencies:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
```

Start MongoDB and the API in one terminal:

```powershell
npm --prefix backend install
Copy-Item backend/.env.example backend/.env
npm run dev:backend
```

In a second terminal, start Streamlit:

```powershell
$env:HEALTHBRIDGE_API_URL = "http://localhost:4000/api"
streamlit run streamlit_app.py
```

Open the local URL printed by Streamlit (usually `http://localhost:8501`). Set the API address using `HEALTHBRIDGE_API_URL` or Streamlit secrets. For local Streamlit secrets, copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and edit it. Never add real secrets to Git.

## Host on Streamlit Community Cloud

1. Push this project folder to a Git repository.
2. Create a Streamlit Community Cloud app and select `streamlit_app.py` as the entry point. Keep `requirements.txt` beside it.
3. Deploy the existing Express API separately on a Node host and MongoDB on a hosted MongoDB service. Set the backend's `MONGODB_URI`, a strong `JWT_SECRET`, and a persistent upload directory if users will upload files.
4. In the Streamlit app's **Settings → Secrets**, set `HEALTHBRIDGE_API_URL = "https://your-api-host.example.com/api"`.

Do not put MongoDB credentials or the JWT signing key in Streamlit secrets. The Streamlit server only needs the public API URL; authenticated user requests use their session token. The supplied heart-globe Earth texture and Unsplash care photos load from their remote image URLs, so the deployed app needs outbound access to those image hosts.

## Optional React frontend

The React + TypeScript frontend is retained in `frontend/` for reference or separate hosting. Its API URL remains configured with `VITE_API_URL`.

## Requirements

- Python 3.10 or newer for Streamlit
- Node.js 20 or newer and npm for the API (and optional React frontend)
- MongoDB Community Server running locally on `127.0.0.1:27017`

On Windows, open **Services** (`services.msc`) and start the **MongoDB Server** service. You can check the listener with `Test-NetConnection 127.0.0.1 -Port 27017` in PowerShell. The backend exits with an error if MongoDB cannot be reached; it does not fall back to browser storage or another database.

## Install and run the API / optional React frontend

From this directory:

```powershell
npm install
npm --prefix backend install
npm --prefix frontend install
Copy-Item backend/.env.example backend/.env
Copy-Item frontend/.env.example frontend/.env
```

Edit `backend/.env`. Keep the local database URI as:

```dotenv
PORT=4000
MONGODB_URI=mongodb://127.0.0.1:27017/healthbridge_ai
JWT_SECRET=replace-with-a-long-random-secret-at-least-24-characters
JWT_EXPIRES_IN=7d
CLIENT_ORIGIN=http://localhost:5173
UPLOAD_DIR=uploads
```

Never commit `.env` files. They are ignored by Git. The frontend only receives `VITE_API_URL`, never the MongoDB URI or JWT signing secret.

Run the backend in a separate terminal. To use the optional React frontend instead of Streamlit, also start Vite:

```powershell
npm run dev:backend
```

```powershell
npm run dev:frontend
```

Or start both from the project root with `npm run dev`. Open <http://localhost:5173> for React. For Streamlit, follow the instructions above. The API health endpoint is <http://localhost:4000/api/health>.

The first backend startup creates the `healthbridge_ai` database and the application collections if missing. It only seeds demo records by their own names and does not drop databases or collections. It creates a demo admin account if that email does not already exist:

- Email: `admin@healthbridge.demo`
- Password: `HealthBridgeDemo!2026`

For a different demo credential, set `DEMO_ADMIN_EMAIL` and `DEMO_ADMIN_PASSWORD` in `backend/.env` before the first startup. This demo password is for local development only.

## Patient journey

1. Register as a patient. Location can be entered manually; GPS is optional.
2. Choose a language and complete the account form.
3. Open **One Journey** to search Chennai facilities for cardiology (or another specialty).
4. Select a demo hospital, choose a future appointment time, and create an appointment request and referral passport.
5. Download a demo PDF passport. The request and referral are saved in MongoDB.
6. Upload documents under **Medical records**. Doctors need explicit patient consent to access them.

Doctor, hospital/clinic, and pharmacy accounts use separate role values. Doctor accounts begin unverified; the demo admin can verify them. Admin access cannot be self-registered.

## API reference

All successful endpoints use `{ "success": true, "message": "...", "data": ... }`. Errors use `{ "success": false, "message": "..." }`. Protected endpoints require `Authorization: Bearer <token>`.

| Method | Endpoint | Access | Purpose |
|---|---|---|---|
| GET | `/api/health` | Public | API and database status |
| POST | `/api/auth/register` | Public | Register patient, doctor, hospital, or pharmacy |
| POST | `/api/auth/login` | Public | Sign in and receive JWT |
| GET | `/api/auth/me` | Signed in | Current account |
| POST | `/api/auth/logout` | Signed in | Client sign-out acknowledgement |
| GET | `/api/dashboard` | Signed in | Role-aware overview |
| GET/PATCH | `/api/patients/me` | Patient | Read/update health and family profile |
| GET | `/api/hospitals` | Public | Search hospitals by `q`, `city`, `specialty`, `page`, `limit` |
| POST | `/api/hospitals` | Admin or hospital | Add a hospital listing |
| GET | `/api/pharmacies` | Public | Browse pharmacy listings |
| GET | `/api/medicines` | Public | Search medicine availability |
| POST | `/api/medicines` | Pharmacy or admin | Add a medicine listing |
| GET | `/api/doctors` | Signed in | List doctor profiles |
| PATCH | `/api/doctors/:id/verification` | Admin | Verify or unverify a doctor |
| GET/POST | `/api/appointments` | Patient, doctor, admin | List allowed appointments / request a visit |
| PATCH | `/api/appointments/:id` | Assigned doctor or admin | Update appointment status |
| GET | `/api/documents` | Patient, consented doctor, admin | List authorized documents |
| POST | `/api/documents/upload` | Patient or consented doctor | Upload PDF, JPEG, PNG, or WebP up to 10 MB |
| GET | `/api/documents/:id/download` | Owner, consented doctor, admin | Download authorized document |
| POST | `/api/consents` | Patient | Grant a doctor all-record or document-specific access |
| PATCH | `/api/consents/:id/revoke` | Patient | Revoke record access |
| GET/POST | `/api/referrals` | Patient (list also admin) | Create/list referral passports |
| GET/POST | `/api/prescriptions` | Patient, doctor, admin | List allowed prescriptions / save with patient-wide consent |
| GET/POST | `/api/notifications` | Signed in | List reminders / schedule a reminder |
| GET | `/api/camps` | Public | List demo health camps |
| GET | `/api/users` | Admin | Paginated account directory |

Lists accept `page` and `limit` (maximum 50). User input is validated with Zod. Uploaded files are stored under `backend/uploads`, kept out of Git, and are served only through an authorization checked download endpoint.

## MongoDB models

Mongoose creates separate collections for `User`, `PatientProfile`, `DoctorProfile`, `Hospital`, `Pharmacy`, `Appointment`, `MedicalDocument`, `Prescription`, `Referral`, `Medicine`, `Notification`, `HealthcareCamp`, and `ConsentRecord`. Models use timestamps, references, enum validation, and indexes for lookup and unique account email.

## Frontend features

- Responsive landing page, role-aware dashboards, hospital finder, appointments, documents, profile and family health, referrals, community information, pharmacy inventory, and admin view.
- Light and dark themes persist in local storage. Language choice persists and covers common navigation and key actions in English, Hindi, Tamil, Telugu, Malayalam, Kannada, Marathi, and Bengali; some detailed demo copy remains English.
- Optional browser location, voice input, and speech output depend on browser support and permission.
- The assistant is a deterministic navigation demo. No external AI service or API key is connected.

## Build

```powershell
npm --prefix frontend run build
```

This checks TypeScript and produces `frontend/dist`.

## Photography and visual references

The landing page gallery uses remote Unsplash images for illustrative purposes. Photos load from `images.unsplash.com`; selecting a photo opens its Unsplash source/search page. Images remain subject to the [Unsplash License](https://unsplash.com/license). The stacked, gently tilted cards and hover zoom take interaction inspiration from the [21st.dev Image Showcase](https://dev.21st.dev/@ravikatiyar162/components/image-showcase). The gallery respects reduced-motion preferences.

## Dashboard and notifications

The signed-in dashboard adapts its shortcuts to the account role, follows the selected language (English, Tamil, Hindi, Telugu, Malayalam, Kannada, Marathi, or Bengali), and labels simulated information. Its CSV export includes only section names, descriptions, and internal routes; it excludes account and health data. The shared Dot Matrix Toaster is mounted once for the whole app, uses generic translated messages, makes no sound, and never displays private health details. Appointment request, status, and document-save actions demonstrate app-wide notifications. The dashboard also has a collapsed notification preview with safe sample messages.

This integration uses the existing React, TypeScript, and CSS setup. No new dependencies or installation steps are required.
