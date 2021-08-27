import queue
import random
import threading
import time
from typing import Optional, Union, Dict

import attr as attr

CMD_REP = ":REP"
CMD_GET = ":GET"
CMD_SET = ":SET"
CMD_ERR = ":ERROR"

CMD_TEMP = ":TEMPERATURE"
CMD_TEMP_EXTREMES = ":TEMPERATURE_EXTREMES"
CMD_TEMP_RESET = ":TEMPERATURE_RESET"
CMD_HUMID = ":HUMIDITY"
CMD_HUMID_EXTREMES = ":HUMIDITY_EXTREMES"
CMD_HUMID_RESET = ":HUMIDITY_RESET"

DEFAULT_TEMPERATURE = 22.0
DEFAULT_HUMIDITY = 56


@attr.s
class TemperatureState:
    temperature: float = attr.ib(validator=attr.validators.instance_of(float), default=DEFAULT_TEMPERATURE)
    max: float = attr.ib(init=False)
    min: float = attr.ib(init=False)

    def __attrs_post_init__(self):
        self.max = self.min = self.temperature

    def update_temperature(self, temperature: float):
        self.temperature = temperature
        if temperature > self.max:
            self.max = temperature
        if temperature < self.min:
            self.min = temperature

    def reset(self):
        self.min = self.max = self.temperature


@attr.s
class HumidityState:
    humidity: int = attr.ib(validator=attr.validators.instance_of(int), default=DEFAULT_HUMIDITY)
    max: int = attr.ib(init=False)
    min: int = attr.ib(init=False)

    def __attrs_post_init__(self):
        self.max = self.min = self.humidity

    def update_humidity(self, humidity: int):
        self.humidity = humidity
        if humidity > self.max:
            self.max = humidity
        if humidity < self.min:
            self.min = humidity

    def reset(self):
        self.min = self.max = self.humidity


class AmbientMonitor:
    def __init__(self):
        self._data_out: Optional[queue.Queue] = None
        self._temperature_state = TemperatureState()
        self._humidity_state = HumidityState()
        self._receive_buffer = bytearray()
        self._command_table: Dict[str, callable] = self._get_command_table()
        self._sim_thread: threading.Thread = threading.Thread(group=None,
                                                              target=self._simulation,
                                                              daemon=True)
        self._data_received = threading.Event()
        self._data_lock = threading.Lock()
        self._data_handler_thread = threading.Thread(group=None,
                                                     target=self._data_handler,
                                                     daemon=True)
        self._sim_thread.start()
        self._data_handler_thread.start()

    def connect(self, data_sink: queue.Queue):
        self._data_out = data_sink

    def disconnect(self):
        self._data_out = None

    def data_received(self, data: bytes) -> int:
        with self._data_lock:
            self._receive_buffer.extend(data)
        self._data_received.set()
        return len(data)

    def _get_command_table(self) -> Dict[str, callable]:
        cmd_table: Dict[str, callable] = {CMD_GET + CMD_TEMP: self._get_temperature,
                                          CMD_GET + CMD_HUMID: self._get_humidity,
                                          CMD_GET + CMD_TEMP_EXTREMES: self._get_temperature_extremes,
                                          CMD_GET + CMD_HUMID_EXTREMES: self._get_humidity_extremes,
                                          CMD_SET + CMD_TEMP_RESET: self._set_reset_temperature,
                                          CMD_SET + CMD_HUMID_RESET: self._set_reset_humidity}
        return cmd_table

    def _get_temperature(self) -> str:
        return CMD_REP+CMD_TEMP+f":{self._temperature_state.temperature:.3f}:!"

    def _get_temperature_extremes(self) -> str:
        return CMD_REP+CMD_TEMP_EXTREMES+f":{self._temperature_state.min:.2f}" \
                                         f":{self._temperature_state.max:.2f}:!"

    def _get_humidity(self) -> str:
        return CMD_REP+CMD_HUMID+f":{self._humidity_state.humidity}:!"

    def _get_humidity_extremes(self) -> str:
        return CMD_REP+CMD_HUMID_EXTREMES+f":{self._humidity_state.min}" \
                                          f":{self._humidity_state.max}:!"

    def _set_reset_temperature(self) -> str:
        self._temperature_state.reset()
        return CMD_REP+CMD_TEMP_RESET + ":!"

    def _set_reset_humidity(self) -> str:
        self._humidity_state.reset()
        return CMD_REP + CMD_HUMID_RESET + ":!"

    def _error_reply(self, msg: str) -> str:
        return CMD_ERR + f":{msg}:!"

    def _data_handler(self):
        while True:
            self._data_received.wait()
            self._data_received.clear()
            while b'!' in self._receive_buffer:
                with self._data_lock:
                    end_idx = self._receive_buffer.index(b'!')
                    command = self._receive_buffer[:end_idx]
                    self._receive_buffer = self._receive_buffer[end_idx+1:]
                    self._parse_command(command)

    def _parse_command(self, command: bytes):
        if command[:1] != b':' or command.count(b':') < 3:
            self._return_reply(self._error_reply("MALFORMED_COMMAND"))
            return
        try:
            command_string = command[:command.index(b':',5)].decode('UTF-8')
            reply = self._command_table[command_string]()
        except UnicodeDecodeError:
            reply = self._error_reply("DECODE_ERROR")
        except ValueError:
            reply = self._error_reply("MALFORMED_COMMAND")
        except KeyError:
            reply = self._error_reply("UNKNOWN_COMMAND")
        self._return_reply(reply)

    def _simulation(self):
        while True:
            self._temperature_state.update_temperature(random.triangular(20.0, 22.0))
            self._humidity_state.update_humidity(random.randint(50, 60))
            time.sleep(0.1)

    def _return_reply(self, reply: str):
        if self._data_out is None:
            return  # not connected
        for c in reply.encode('UTF-8'):
            self._data_out.put(c)


