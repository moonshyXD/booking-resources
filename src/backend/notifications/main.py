from fastapi import FastAPI
import uvicorn

from notifications.adapters.rest.smtp import router as smtp_router

app = FastAPI()


@app.get("/")
async def greet():
    return {"message": "Hello World"}

app.include_router(smtp_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8011)
