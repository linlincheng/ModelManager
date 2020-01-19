# here stores some useful helper functions


def get_current_datetime():
    # get current datetime string
    # return: dictionary with current_time object and string version
    from datetime import datetime

    now = datetime.now()
    current_time_dict = {
        'current_time': now.strftime('%Y-%m-%d %H:%M'),
        'current_time_underscore': now.strftime('%Y_%m_%d_%H_%M_%S')
    }
    return(current_time_dict)


def retrieve_name(var):
    # print variable names
    import inspect
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var]


def verify_and_create_dir(directory):
    # check if dir exists, create if not
    import os
    if not os.path.exists(directory):
        print("directory doesn't exist, creating now: {}".format(directory))
        os.makedirs(directory)
    return


def pickle_save(object_file, file_path):
    import pickle
    # concat model file name
    object_name = retrieve_name(object_file).pop()
    print(object_name)
    print(type(object_name))
    # verify dir
    verify_and_create_dir(file_path)          
    print('Saving object {object_file}: {path}...'.format(object_file=object_file,
                                                          path=file_path))
    object_path = file_path + '/'+object_name+'.pickle'
    with open(object_path, "wb") as output_file:
        pickle.dump(object_file, file=output_file)
    return


def pickle_load(object_name, file_path):
    import pickle
    # concat model file name
    # object_name = retrieve_name(object_file)
    print('Loading object {object_name}: {path}...'.format(object_name=object_name,
                                                           path=file_path))                                           
    object_path = file_path + '/'+object_name+'.pickle'
    with open(object_path, "wb") as output_file:
        loaded_object = pickle.load(object_file, file=output_file)
    return(loaded_object)
