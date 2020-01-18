# here stores some useful helper functions

def get_current_datetime():

    # return: dictionary with current_time object and string version
    from datetime import datetime

    now = datetime.now()
    dt_string = now.strftime('%Y_%m_%d_%H_%M_%S')
    current_time_dict = ({
        "current_time": now,
        "current_time_string": dt_string
    })
    return(current_time_dict)     