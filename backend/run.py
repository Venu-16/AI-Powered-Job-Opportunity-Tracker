#!/usr/bin/env python3
import sys
import os
print("Starting run.py")
print("Current dir:", os.getcwd())
sys.path.insert(0, os.path.dirname(__file__))

try:
    from app.main import app
    print("App imported successfully")
except Exception as e:
    print(f"Import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
