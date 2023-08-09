import zmq
import multiprocessing

def sub1():
    context = zmq.Context()

    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://localhost:5556")
    subscriber.setsockopt(zmq.SUBSCRIBE, b"123")

    while True:
        topic, message = subscriber.recv_multipart()
        print(f"Subscriber 1 received: {message.decode('utf-8')}, {topic}")

def sub2():
    context = zmq.Context()

    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://localhost:5556")
    subscriber.setsockopt(zmq.SUBSCRIBE, b"weather")

    while True:
        topic, message = subscriber.recv_multipart()
        print(f"Subscriber 2 received: {message.decode('utf-8')}")


if __name__ == '__main__':
    multiprocessing.Process(target=sub1).start()
    multiprocessing.Process(target=sub2).start()