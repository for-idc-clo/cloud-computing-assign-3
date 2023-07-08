from fastapi import FastAPI, HTTPException, Request, status, Depends
from fastapi.responses import PlainTextResponse
from fastapi.exceptions import RequestValidationError
from dishes.router import router as dishes_router
from meals.router import router as meal_router


def validate_content_type(request: Request):
    if (
        request.method in ["POST", "PUT", "PATCH", "DELETE"]
        and request.headers.get("Content-type") != "application/json"
    ):
        raise HTTPException(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="0")


app = FastAPI(dependencies=[Depends(validate_content_type)])

app.include_router(dishes_router, prefix="/dishes")
app.include_router(meal_router, prefix="/meals")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    if exc.errors()[0]["type"] == "type_error.dict":
        return PlainTextResponse(
            "0",
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        )

    if exc.errors()[0]["type"] == "value_error.missing":
        return PlainTextResponse(
            "-1",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    return request.app.handle_exception(request, exc)


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(_, exc):
    if exc.status_code == status.HTTP_415_UNSUPPORTED_MEDIA_TYPE:
        return PlainTextResponse(
            "0", status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
        )
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)
