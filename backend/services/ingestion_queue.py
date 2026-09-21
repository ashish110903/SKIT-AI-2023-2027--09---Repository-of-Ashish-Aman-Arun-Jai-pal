import queue

telemetry_queue = queue.Queue(maxsize=10000)

def enqueue_packet(data: dict):
    if not telemetry_queue.full():
        telemetry_queue.put(data)
