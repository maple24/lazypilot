from fastapi import FastAPI
import multiprocessing
import queue
import zmq
import uvicorn
from loguru import logger
from pydantic import BaseModel
import json
from typing import Dict, Union


class Message(BaseModel):
    topic: str
    action: Dict[str, Union[str, dict]]


class TestMsg(BaseModel):
    message: str


app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Hello world"}


@app.post("/test/")
async def test(message: TestMsg):
    return {"result": message}


@app.post("/publish/")
async def publish_message(message: Message):
    app.publisher.send_multipart(
        [message.topic.encode(), json.dumps(message.action).encode()]
    )
    logger.success(f"Message published: {message}")
    try:
        result = app.queue.get(timeout=5)  # Wait for 5 seconds
        return {"result": result}
    except queue.Empty:
        return {"result": "No result available within the timeout."}


def run_fastapi(queue: multiprocessing.Queue):
    context = zmq.Context()
    app.publisher = context.socket(zmq.PUB)
    app.publisher.bind("tcp://*:5556")
    app.queue = queue
    uvicorn.run(app, host="0.0.0.0", port=1234)


if __name__ == "__main__":
    q = multiprocessing.Queue()

    # Start FastAPI server in a separate process
    fastapi_process = multiprocessing.Process(target=run_fastapi, args=(q,))
    fastapi_process.start()
    fastapi_process.join()
