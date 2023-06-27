import functools
import threading
import time
import traceback
from typing import Callable

from starrail.utils import loggings

logger = loggings.get_logger(__file__)


class IntervalThread(threading.Thread):

    def __init__(self, interval: float, func: Callable):
        super().__init__(daemon=True)
        self.interval = interval
        self.func = func
        self.stop_event = threading.Event()

    def run(self):
        while not self.stop_event.is_set():
            start_time = time.time()
            try:
                self.func()
            except Exception:
                logger.error(traceback.format_exc())
            end_time = time.time()
            wait_time = start_time - end_time + self.interval
            if wait_time > 0:
                self.stop_event.wait(wait_time)

    def stop(self):
        self.stop_event.set()


def set_interval(
    interval: float,
    func: Callable,
    *args,
    **kwargs,
) -> IntervalThread:
    """
    Starts and returns an interval-based thread that executes the provided
    callable at each interval.

    Args:
        interval (float): The time interval between each execution of the
            callable in seconds.
        func (callable): The function to be executed at each interval.
        *args: Variable-length argument list to be passed to the callable.
        **kwargs: Arbitrary keyword arguments to be passed to the callable.

    Returns:
        IntervalThread: An instance of the interval-based thread.
    """

    _callable = functools.partial(func, *args, **kwargs)
    thread = IntervalThread(interval=interval, func=_callable)
    thread.start()

    return thread
