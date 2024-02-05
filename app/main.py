from fastapi import FastAPI
from .routers.route_fule_optimization_for_good_weather_ import router as fuel_cons_router

app = FastAPI()

# me fuel cons model route 
app.include_router(fuel_cons_router)
