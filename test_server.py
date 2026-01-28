import sys
import traceback

try:
    import uvicorn
    print("✓ Uvicorn imported")
    
    from app.main import app
    print("✓ App imported")
    
    print("\nStarting server on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print("\nFull traceback:")
    traceback.print_exc()
    sys.exit(1)
