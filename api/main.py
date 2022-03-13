from devtools import debug
from fastapi import FastAPI, Response, status
from starlette.responses import RedirectResponse

from api.database import client
from api.routers import exercises

app = FastAPI()

app.include_router(exercises.router)

# use devtools.debug() instead of print()


@app.get("/", include_in_schema=False)
def read_root():
    """Redirect root access to swagger docs."""
    return RedirectResponse("/docs")


@app.get("/health", tags=["health check"])
async def health_check(response: Response):
    try:
        db_results = await client.server_info()
        debug(db_results)
        if db_results:
            return {"healthy": True}
    except Exception:
        pass

    response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return {"healthy": False}
