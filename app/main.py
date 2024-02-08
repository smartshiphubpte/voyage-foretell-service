from fastapi import FastAPI
from .routers.route_fuel_optimization_for_good_weather_ import router as fuel_cons_router

app = FastAPI(
    docs_url="/voyage-foretell-service-be/docs",
    openapi_url="/voyage-foretell-service-be/openapi.json"
)

# me fuel cons model route 
app.include_router(fuel_cons_router)
