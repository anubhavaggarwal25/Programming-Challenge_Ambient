import AmbientAPI as ambient_api

if __name__ == '__main__':

    rate = 0.1
    #
    # Creating an object of Ambient API
    #
    monitor = ambient_api.AmbientAPI(rate)
    #
    # Reset the Temperature value
    #
    reset_temp = monitor.reset_temperature()
    print('Reset the temperature value')
    print(reset_temp)
    print()
    #
    # Reset the Humidity value
    #
    reset_hum = monitor.reset_humidity()
    print('Reset the humidity value')
    print(reset_hum)
    print()
    #
    # get the current temperature value
    #
    curr_temp = monitor.get_temperature()
    print("current temperature ")
    print(curr_temp)
    print()
    #
    # get the list of temperature values
    #
    curr_temp_list = monitor.get_temperature_extremes()
    print("current temperature List")
    print(curr_temp_list)
    print()
    #
    # get the current humidity value
    #
    curr_hum = monitor.get_humidity()
    print("current humidity ")
    print(curr_hum)
    print()
    #
    # get the list of current humidity values
    #
    curr_hum_list = monitor.get_humidity_extremes()
    print("current humidity List ")
    print(curr_hum_list)
    print()
