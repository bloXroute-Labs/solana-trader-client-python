import threading

class RequestIDManager():
    _id: int
    _lock: threading.Lock

    def __init__(self):
        self._id = 1
        self._lock = threading.Lock()

    def next(self) -> int:
        self._lock.acquire()

        current_id = self._id
        self._id += 1

        self._lock.release()

        return current_id