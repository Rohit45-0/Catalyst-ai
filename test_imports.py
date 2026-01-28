try:
    from app.api import auth, projects, uploads, jobs, assets
    print("Imports successful!")
except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"Error: {e}")
