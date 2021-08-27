# Ambient-Temperature-Monitoring Device #
This repository contains the implementation of a simple simulated Ambient-Temperature-Monitoring device.

The device's functionality is exported via a string based communication protocol which can be accessed via a Serial like interface
### What is this repository for? ###
The aim of this repository is to provide a self-contained 'virtual' device that can 
easily be shared and used as a sandbox for programming challenges at different levels of complexity.



## Protocol Specification ##
The protocol to communicate with the Ambient-Temperature-Monitoring Device is based
on a Request-Response pattern. All communication is initiated by the host and the device
answers with exactly one response.

#### Commmand Structure ####
    :GET:CMD:!
    :SET:CMD[:VALUE]:!
#### Reply Structure ####
    :REP:CMD[:VALUE]...[:VALUE]:!
    :ERROR[:MSG]:!
#### Get Commands ####
Command | Reply Value Type | Reply
--------|------------|------
`:GET:TEMPERATURE:!` | Float | `:REP:TEMPERATURE:21.2123:!`
`:GET:TEMPERATURE_EXTREMES:!` | List[Float] | `:REP:TEMPERATURE_EXTREMES:12.21:27.23123:!`
`:GET:HUMIDITY:!` | Integer | `:REP:HUMIDITY:56:!`
`:GET:HUMIDITY_EXTREMES:!`| List[Integer] | `:REP:HUMIDITY_EXTREMES:23:76:!`
#### Set Commands ####
Command | Reply Value Type | Reply
--------|------------|---------
`:SET:TEMPERATURE_RESET:!` | None | `:REP:TEMPERATURE_RESET:!`
`:SET:HUMIDITY_RESET:!` | None | `:REP:HUMIDITY_RESET:!`

### Example ###
    interface = ComInterfaceAmbientMonitor(timeout=0.5)
    interface.write(":GET:TEMPERATURE:!".encode('UTF-8'))
    # wait for data to be available
    reply = interface.read(interface.in_waiting)
    print(reply)  # --> b':REP:TEMPERATURE:21.2123:!'



