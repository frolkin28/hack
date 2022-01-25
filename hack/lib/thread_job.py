import asyncio
import threading
import typing as t


class ThreadJob(threading.Thread):
    def __init__(
        self,
        callback: t.Callable,
        interval: int
    ) -> None:
        self.async_callback = callback
        self.event = threading.Event()
        self.interval = interval
        super(ThreadJob, self).__init__()

    def run(self) -> None:
        while not self.event.wait(self.interval):
            asyncio.run(self.async_callback())

    def remove(self) -> None:
        self.event.set()
