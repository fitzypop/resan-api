from fastapi import FastAPI, Response, status
from starlette.responses import RedirectResponse

from api.database import health_check as db_health_check
from api.routers import exercises, sign_up, users

app = FastAPI(title="Resan API")
app.include_router(exercises.router)
app.include_router(sign_up.router)
app.include_router(users.router)


@app.get("/", include_in_schema=False)
def read_root():
    """Redirect root access to swagger docs."""
    return RedirectResponse("/docs")


@app.get("/health", tags=["health check"], status_code=200)
async def health_check(response: Response):
    try:
        db_results = await db_health_check()
        if db_results:
            result = {"healthy": True, "db_status": "ok" if db_results["ok"] else "bad"}
        else:
            raise Exception()
    except Exception:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        result = {"healthy": False, "db_status": "not connected"}

    return result
