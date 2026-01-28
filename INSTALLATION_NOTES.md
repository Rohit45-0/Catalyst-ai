# Installation Notes

## Fixed Issues

1. **Database Engine**: Made engine creation lazy to avoid import-time errors
2. **Email Validation**: Changed from `EmailStr` to `str` with custom validation (install `email-validator` for full email validation)
3. **API Routes**: All routes are now properly configured

## Remaining Issue: psycopg2-binary

The `psycopg2-binary` package may have installation issues. To fix:

### Option 1: Reinstall psycopg2-binary
```powershell
# Activate your virtual environment first
.\venv\Scripts\Activate.ps1

# Uninstall and reinstall
pip uninstall psycopg2-binary -y
pip install psycopg2-binary
```

### Option 2: Use the fix script
Run the provided `fix_psycopg2.ps1` script (may require Administrator privileges)

### Option 3: Install missing packages
```powershell
.\venv\Scripts\Activate.ps1
pip install email-validator
pip install --upgrade --force-reinstall psycopg2-binary
```

## Running the Application

Once dependencies are installed:

```powershell
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

The application should start successfully. If you see database connection errors, make sure:
1. PostgreSQL is running
2. The DATABASE_URL in `.env` is correct
3. The database `catalyst_ai` exists
