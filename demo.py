import time

from ambient_monitor import ComInterfaceAmbientMonitor

if __name__ == "__main__":
    with ComInterfaceAmbientMonitor() as interface:
        for i in range(20):
            interface.write(':GET:TEMPERATURE:!'.encode('UTF-8'))
            time.sleep(0.1)
            reply = interface.read(interface.in_waiting).decode('UTF-8')
            print(reply)