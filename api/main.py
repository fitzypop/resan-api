from fastapi import FastAPI, Response, status
from starlette.responses import RedirectResponse

from api.database import health_check, manage_db
from api.routers import exercises, sign_up, users
from api.settings import api_settings

app = FastAPI(title=api_settings.title)
app.include_router(exercises.router)
app.include_router(sign_up.router)
app.include_router(users.router)


@app.on_event("startup")
async def startup_event():
    await manage_db()


@app.get("/", include_in_schema=False)
def read_root():
    """Redirect root access to swagger docs."""
    return RedirectResponse("/docs")


@app.get("/health", tags=["health check"], status_code=200)
async def get_health_check(response: Response):
    try:
        db_results = await health_check()
        if db_results:
            result = {"healthy": True, "db_status": "ok" if db_results["ok"] else "bad"}
        else:
            raise Exception()
    except Exception:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        result = {"healthy": False, "db_status": "not connected"}

    return result
