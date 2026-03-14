from fastapi import FastAPI

from adapters.rest.auth import router as auth_router

app = FastAPI()

app.include_router(auth_router)


@app.get("/")
def greet():
    return {"data": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", port=8001, reload=True)
