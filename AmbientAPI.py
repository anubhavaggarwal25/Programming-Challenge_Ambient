import time
import re

from ambient_monitor import ComInterfaceAmbientMonitor

class AmbientAPI:
    def __init__(self, rate):
        self.rate = rate
    #
    # Get the current temperature value fromt he Ambient monitor interface
    # returns a float value
    #
    def get_temperature(self) -> float:
        reply = ''
        current_temperature = 0.0
        with ComInterfaceAmbientMonitor() as interface:
            interface.write(':GET:TEMPERATURE:!'.encode('UTF-8'))
            time.sleep(self.rate)
            reply = interface.read(interface.in_waiting).decode('UTF-8')
            current_temperature = float(re.findall(r"[-+]?\d*\.\d+|\d+", reply)[0])

        return current_temperature
    #
    # Get the list of current temperature values from the Ambient monitor interface
    # returns a list of float values
    #
    def get_temperature_extremes(self) -> list[float]:
        reply = ''
        current_temperature_list = []
        with ComInterfaceAmbientMonitor() as interface:
            interface.write(':GET:TEMPERATURE_EXTREMES:!'.encode('UTF-8'))
            time.sleep(self.rate)
            reply = interface.read(interface.in_waiting).decode('UTF-8')
            for value in re.findall(r"[-+]?\d*\.\d+|\d+", reply):
                current_temperature_list.append(float(value))
        return current_temperature_list
    #
    # Get the current humidity value from the Ambient monitor interface
    # returns a integer value
    #
    def get_humidity(self) -> int:
        reply = ''
        current_humidity = 0
        with ComInterfaceAmbientMonitor() as interface:
            interface.write(':GET:HUMIDITY:!'.encode('UTF-8'))
            time.sleep(self.rate)
            reply = interface.read(interface.in_waiting).decode('UTF-8')
            current_humidity = int(re.findall(r"[-+]?\d*\.\d+|\d+", reply)[0])

        return current_humidity
    #
    # Get the list of current humidity values from the Ambient monitor interface
    # returns a list of integer values
    #
    def get_humidity_extremes(self) -> list[int]:
        reply = ''
        current_humidity_list = []
        with ComInterfaceAmbientMonitor() as interface:
            interface.write(':GET:HUMIDITY_EXTREMES:!'.encode('UTF-8'))
            time.sleep(self.rate)
            reply = interface.read(interface.in_waiting).decode('UTF-8')
            for value in re.findall(r"[-+]?\d*\.\d+|\d+", reply):
                current_humidity_list.append(int(value))

        return current_humidity_list
    #
    # Reset the temperature value to default value
    # returns a reply that the temperature value is reset
    #
    def reset_temperature(self) -> str:
        with ComInterfaceAmbientMonitor() as interface:
            interface.write((':SET:TEMPERATURE_RESET:!').encode('UTF-8'))
            time.sleep(self.rate)
            reply = interface.read(interface.in_waiting).decode('UTF-8')

        return reply
    #
    # Reset the humidity value to default value
    # returns a reply that the humidity value is reset
    #
    def reset_humidity(self) -> str:
        with ComInterfaceAmbientMonitor() as interface:
            interface.write((':SET:HUMIDITY_RESET:!').encode('UTF-8'))
            time.sleep(self.rate)
            reply = interface.read(interface.in_waiting).decode('UTF-8')

        return reply
    #
    # Set the temperature value
    # returns the reply that the temperature is reseted
    # Status -> not working
    #
    def set_temperature(self, value) -> str:
        with ComInterfaceAmbientMonitor() as interface:
            interface.write((f':SET:TEMPERATURE[:{value}]:!').encode('UTF-8'))
            time.sleep(self.rate)
            reply = interface.read(interface.in_waiting).decode('UTF-8')

        return reply
    #
    # Set the humidity value
    # returns the reply that the humidity is reseted
    # Status -> not working
    #
    def set_humidity(self, value) -> str:
        with ComInterfaceAmbientMonitor() as interface:
            interface.write((f':SET:HUMIDITY[:{value}]:!').encode('UTF-8'))
            time.sleep(self.rate)
            reply = interface.read(interface.in_waiting).decode('UTF-8')

        return reply
