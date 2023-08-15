# lazypilot
![preview](assets/preview.png)

## architecture
![architecture](assets/lazypilot.png)
- zeroMQ to publish message to processes with [topic, message]
- multiprocessing queue to get response back
- fastapi to provide restapi interface

## test
curl -X POST -H "Content-Type: application/json" -d '{"message": "helloworld"}' http://localhost:1234/test/

curl -X GET http://localhost:1234/

curl -X POST -H "Content-Type: application/json" -d '{"topic": "webcam", "action": {"method": "compare", "params": {"method": "compare", "params": {"name": ""}}}}' http://localhost:8000/update_message/

curl -X POST http://localhost:1234/publish/YourMessageHere