import uvicorn
import sys
from pathlib import Path

# Add backend to python path explicitly
root_dir = Path(__file__).resolve().parent
sys.path.append(str(root_dir / "backend"))

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=False)