import logging
import traceback

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_CONTENT

from app.core.exceptions import ConflictError, DomainError, NotFoundError

logger = logging.getLogger(__name__)

class ExceptionHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except NotFoundError as exc:
            logger.warning("Not found: %s", exc.message)
            return JSONResponse(status_code=HTTP_404_NOT_FOUND, content={"detail": exc.message})
        except ConflictError as exc:
            logger.warning("Conflict: %s", exc.message)
            return JSONResponse(status_code=409, content={"detail": exc.message})
        except DomainError as exc:
            logger.warning("Domain error: %s", exc.message)
            return JSONResponse(status_code=HTTP_422_UNPROCESSABLE_ENTITY, content={"detail": exc.message})
        except Exception as exc:
            logger.error("Unhandled exception: %s", traceback.format_exc())
            return JSONResponse(status_code=500, content={"detail": "Internal server error"})
