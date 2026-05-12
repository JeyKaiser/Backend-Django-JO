# Backend Structure

This repository keeps two backend entrypoints for compatibility:

- `backend/manage.py` is the active entrypoint used during development.
- `backend/Backend/manage.py` is a legacy/deployment-compatible copy that mirrors the same project settings.

## Active apps

- `JO_System_Project/`: Django project settings, root URLs, startup checks.
- `usuarios/`: Authentication pages plus the user API used by the frontend.
- `users/`: Legacy API layer for user CRUD and database health.
- `costeo_app/`: Core collection, reference, traceability, and dimensional data endpoints.
- `consumos/`: Consumption endpoints.
- `sap/`: SAP/HANA integration layer and read-only service adapters.

## Structure notes

- API routes are centralized in the app `urls.py` files whenever possible.
- The HANA read-only rule lives in `sap/services.py`.
- MySQL is the writable database for the application runtime.
- `Backend/` is kept only for compatibility. Prefer editing the top-level `backend/` package unless a deployment target explicitly requires the legacy copy.

## Recommended entrypoint

```bash
cd backend
source .venv310/bin/activate
python manage.py runserver
```
