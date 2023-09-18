from fastapi import FastAPI

def add_multiple_routes(app: FastAPI, routes: list):
    for route in routes:
        app.include_router(route)
    
