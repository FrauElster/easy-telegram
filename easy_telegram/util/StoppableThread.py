# type: ignore
import ctypes
import threading
from logging import getLogger
from threading import Thread
logger = getLogger('StoppableThread')


class StoppableThread(Thread):
    """
    This thread returns the target return value on join.
    If "stop()" is called, it terminates the thread.
    """

    class StopSignal(Exception):
        pass  # pylint: disable=W0107

    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        if kwargs is None:
            kwargs = {}
        self._return = None

    def run(self) -> None:
        """
        Executes the target function
        :return:
        """
        if self._target is not None:
            try:
                self._return = self._target(*self._args, **self._kwargs)
            except StoppableThread.StopSignal:
                logger.debug("Stopped thread '%s'", self.name)
            except Exception as err:
                logger.exception("'%s' occurred in thread %s: %s", err.__class__.__name__, self.name, err)
                raise err

    def get_id(self) -> int:
        """
        :return: the threads id
        """
        if hasattr(self, "_thread_id"):
            return self._thread_id  # pylint: disable=E1101
        for id_, thread in threading._active.items():  # pylint: disable=W0212
            if thread is self:
                setattr(self, "_thread_id", id_)
                return id_

    def stop(self) -> None:
        """
        Terminates the thread

        This works a little bit complicated, through injecting a exception on c level into the run method
        :return:
        """
        thread_id: int = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_ulong(thread_id),
                                                         ctypes.py_object(StoppableThread.StopSignal))
        if res > 1:
            ctypes.pythonapi.PythonThreadState_SetAsyncExc(thread_id, 0)

    def join(self, timeout=None):
        """
        Waits for the thread to finish and forwards the return value of the target function
        :param timeout:
        :return:
        """
        Thread.join(self, timeout)
        return self._return
