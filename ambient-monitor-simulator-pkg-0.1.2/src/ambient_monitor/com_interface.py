import queue
import time
from queue import Empty
from typing import Union, Optional

from .ambient_monitor import AmbientMonitor


class ComInterfaceAmbientMonitor:
    """Communication Interface to the AmbientMonitor, modeled on basis of pySerial interface"""
    def __init__(self, timeout: float = None):
        self._read_timeout: Optional[float] = timeout  # Read timeout - None => blocking indefinitely
        self._data_out_q = queue.Queue()
        self._consumer = AmbientMonitor()
        self.open()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, type, value, traceback):
        self._consumer.disconnect()

    def open(self):
        """Connect the interface to the consumer of the data that implements the behavior/reaction"""
        self._consumer.connect(self._data_out_q)

    def read(self, size: int = 1) -> bytes:
        """Read size bytes from the serial port.

        If a timeout is set it may return less characters as requested.
        With no timeout it will block until the requested number of bytes is read."""
        if self._read_timeout is None:
            data = bytearray()
            while len(data) < size:
                data.append(self._data_out_q.get())
        else:
            data = self._gather_data(size, self._read_timeout)

        return bytes(data)

    def write(self, data: bytes) -> int:
        """Write the bytes data to the port.

        This should be of type bytes (or compatible such as bytearray or memoryview).
        Unicode strings must be encoded (e.g. 'hello'.encode('utf-8')."""
        assert isinstance(data, bytes)
        self._consumer.data_received(data)
        return len(data)

    @property
    def in_waiting(self) -> int:
        """Return the number of bytes in the receive buffer."""
        return self._data_out_q.qsize()

    @property
    def timeout(self) -> Union[float, None]:
        """Get current read timeout setting"""
        return self._read_timeout

    @timeout.setter
    def timeout(self, timeout: Union[float, None]):
        """Set read timeout"""
        self._read_timeout = timeout

    def _gather_data(self, size: int, timeout: float) -> bytes:
        assert isinstance(timeout, float)
        data = bytearray()
        start = time.time()
        while len(data) < size and time.time() - start < timeout:
            try:
                data.append(self._data_out_q.get(timeout=0.01))
            except Empty:
                pass
        return data