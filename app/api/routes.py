from fastapi import FastAPI, APIRouter


def add_multiple_routes(app: FastAPI, routes: list[APIRouter]):
    for route in routes:
        app.include_router(route)
