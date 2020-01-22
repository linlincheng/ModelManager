# here stores some useful helper functions
import os
import pickle
from datetime import datetime
import inspect


def get_current_datetime():
    # get current datetime string
    # return: dictionary with current_time object and string version
    now = datetime.now()
    current_time_dict = {
        'current_time': now.strftime('%Y-%m-%d %H:%M'),
        'current_time_underscore': now.strftime('%Y_%m_%d_%H_%M_%S')
    }
    return(current_time_dict)


def retrieve_name(var):
    # print variable names
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var]


def verify_and_create_dir(directory):
    # check if dir exists, create if not
    if not os.path.exists(directory):
        print("directory doesn't exist, creating now: {}".format(directory))
        os.makedirs(directory)

def pickle_save_model(model_object, file_path):
    # verify dir
    verify_and_create_dir(file_path)
    file_path = file_path+'model.pickle'
    print('Saving object: {path}...'.format(path=file_path))
    with open(file_path, "wb") as output_file:
        pickle.dump(model_object, file=output_file)


def pickle_load_model(file_path):
    # TODO: add empty object
    file_path = file_path+'model.pickle'
    # concat model file name
    print('Loading object {path}...'.format(path=file_path))
    # check file
    os.path.isfile(file_path)
    with open(file_path, "rb") as output_file:
        try:
            loaded_object = pickle.load(file=output_file)
        except EOFError as err:
            print('model.pickle object is empty in the specified path, please check...')
            raise err
    return(loaded_object)
