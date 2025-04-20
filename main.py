import argparse
import uvicorn
from app.config import API_HOST, API_PORT

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SHL Assessment Recommendation System")
    parser.add_argument("--mode", type=str, choices=["api", "web"], default="web",
                      help="Run in API mode or web interface mode")
    args = parser.parse_args()
    
    if args.mode == "api":
        # Run FastAPI
        uvicorn.run("api:app", host=API_HOST, port=API_PORT, reload=True)
    