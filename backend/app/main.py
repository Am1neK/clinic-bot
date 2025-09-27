from fastapi import FastAPI
import uvicorn
from backend.app.api import webhook, bookings

app = FastAPI()
app.include_router(webhook.router, prefix="/webhook")
app.include_router(bookings.router, prefix="/api/bookings")

@app.get("/")
def root():
    return {"status":"ok"}

if __name__ == "__main__":
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
