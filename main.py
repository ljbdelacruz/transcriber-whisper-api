# main.py
# Entry point for the application

# Import the FastAPI app from app.main
from app.main import app

# This allows running the app with 'uvicorn main:app'

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)
