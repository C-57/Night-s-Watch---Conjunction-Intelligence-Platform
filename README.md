# SSA Conjunction Intelligence — Setup Guide

## Structure

```
ssa/
├── app.py              ← Flask proxy (talks to Space-Track)
├── requirements.txt
└── ssa_dashboard.html  ← Open this in your browser
```

## Step 1 — Install dependencies

```bash
pip install -r requirements.txt | py -m pip install -r requirements.txt
```

## Step 2 — Run the proxy

```bash
python app.py | py app.py
```

You should see:
```
🛰  SSA Proxy running on http://localhost:5001
```

## Step 3 — Open the dashboard

Open `ssa_dashboard.html` in your browser (double-click or drag into Chrome/Firefox).

## Step 4 — Enter credentials

Use your own Space-Track.org login. No account? Register free at:
https://www.space-track.org/auth/createAccount

## Step 5 — Run analysis

Default NORAD IDs are pre-filled (Pixxel Firefly 1/2/3 + Cartosat-3).
Hit RUN ANALYSIS.

---

## How it works

```
Browser  →  localhost:5001/proxy/login   →  space-track.org (login)
Browser  →  localhost:5001/proxy/tle     →  space-track.org (TLE fetch)
```

The proxy holds the authenticated session cookie so your browser
doesn't have to deal with Space-Track's CORS restrictions.

---

## If proxy is not running

The dashboard falls back to realistic mock TLE data automatically
so you can demo the UI without any backend.

---

## Next steps (v0.2)

- [ ] Replace simplified propagator with satellite.js (full SGP4)
- [ ] Add real covariance from Space-Track CDM endpoint
- [ ] Auto-refresh TLEs every 6 hours
- [ ] Export conjunction report as PDF
