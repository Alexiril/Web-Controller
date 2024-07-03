from threading import Lock

class LockObject[T]:

    
    def __init__(self, datatype: type[T], *args: ...) -> None:
        self._lock: Lock = Lock()
        self._data = datatype(*args)

    def __enter__(self) -> T:
        self._lock.acquire()
        return self._data
    
    def __exit__(self, exception_type, exception_value, exception_traceback) -> None:
        self._lock.release()
        if exception_value != None:
            from core.Exceptions import LockObjectException
            raise LockObjectException(
                exception_type,
                exception_value,
                exception_traceback)
    
    def reset(self, data: T) -> None:
        with self._lock:
            self._data = data