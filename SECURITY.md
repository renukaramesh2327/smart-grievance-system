# Security & Architecture

This document clarifies the security posture for auditors and reviewers.

## Two Distinct Modes

| Mode | Path | Data Storage | Auth |
|------|------|--------------|------|
| **Full app** | `frontend/` + Flask backend | PostgreSQL/SQLite | JWT, server-side |
| **Static demo** | `docs/` | localStorage only | Simulated, client-only |

**The `docs/` folder is a standalone demo for GitHub Pages.** It does not use the backend. Any audit of "client-side persistence" or "JS-only auth" applies to `docs/` only.

---

## Full App (frontend/ + backend/) — Production Architecture

### Data & Persistence

- **Database:** SQLAlchemy with PostgreSQL (production) or SQLite (development)
- **Complaints, users, roles, lockouts, fraud flags:** Stored server-side only
- **localStorage usage:** JWT token + cached user object for display; language preference

### Authentication & Authorization

- **JWT** issued by backend; validated on every protected request
- **Role checks:** Enforced server-side via `get_current_user_from_token()` and role guards
- **Lockout:** 3 failed logins = 24-hour lockout per email (server-side, `FailedLoginAttempt` table)
- **Passwords:** Werkzeug `generate_password_hash` / `check_password_hash` (PBKDF2)

### Validation & Sanitization

- **Input validation:** Server-side for all API inputs
- **XSS:** `bleach` sanitization via `SecurityFirewall.validate_input()` before persistence
- **SQL injection:** Parameterized queries (SQLAlchemy ORM); blocked patterns in firewall

### Rate Limiting & Throttling

- IP-based limits on login (10/5 min), registration (5/10 min), grievance submission (20/hour)
- IP blocking after repeated suspicious activity

### ML & Fraud Detection

- **Classification:** scikit-learn TF-IDF + Logistic Regression (~74% accuracy), runs server-side
- **Content moderation:** Server-side keyword/heuristic checks before persistence
- **No "95%+" claim** in current README

### CSRF

- JWT in `Authorization` header (not cookies) — not vulnerable to classic CSRF
- No cookie-based session auth

---

## Known Gaps & Recommendations

1. **Frontend innerHTML:** User content is sanitized server-side before storage; frontend uses `innerHTML` for rendering. Consider escaping or using `textContent` for user-generated fields to defense-in-depth.

2. **Demo credentials:** `admin123`, `officer123` in README/seed — for development only. Rotate before any real deployment.

3. **CORS:** Currently `origins: "*"` in development. Restrict to specific domain in production.

4. **Audit logging:** Basic security logging exists; consider structured audit trail for compliance.

---

## For Auditors

- **Full app:** Run `python run.py` and use http://localhost:8000 (serves `frontend/`).
- **Static demo:** The `docs/` folder is for GitHub Pages only; it is not the production app.
- **Backend code:** See `backend/routes/`, `backend/security/`, `backend/services/`.
