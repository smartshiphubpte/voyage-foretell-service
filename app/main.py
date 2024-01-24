from fastapi import FastAPI
from .routers.PredictMeFuelConsRoutes import router as fuel_cons_router

app = FastAPI()

# me fuel cons model route 
app.include_router(fuel_cons_router)
