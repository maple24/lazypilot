from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import multiprocessing


# FastAPI setup
app = FastAPI()


class Message(BaseModel):
    message: str


@app.get("/")
async def read_root():
    return {"message": "FastAPI is running!"}


@app.post("/update_message/")
async def update_message(message: Message):
    app.queue.put(message.message)  # Put the message in the queue
    return {"message": "Message updated successfully"}


def run_fastapi(queue):
    app.queue = queue  # Attach the queue to the FastAPI app
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == '__main__':
    run_fastapi(queue=multiprocessing.Queue())