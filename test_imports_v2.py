import sys
import traceback

print("Starting import test...")
try:
    print("Importing auth...")
    from app.api import auth
    print("Importing projects...")
    from app.api import projects
    print("Importing uploads...")
    from app.api import uploads
    print("Importing jobs...")
    from app.api import jobs
    print("Importing assets...")
    from app.api import assets
    print("All imports successful!")
except Exception:
    print("An error occurred during imports:")
    traceback.print_exc()
    sys.exit(1)
