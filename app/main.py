from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import chart_router, location_router, chat_router

# Create app
app = FastAPI(
    title="JStar Astrology API",
    description="Astrology and Synastry calculation engine",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(chart_router)
app.include_router(location_router)
app.include_router(chat_router)


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
