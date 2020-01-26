# Testing local io using mock
# test/model_deployment.json and test/.modelMasterTable.csv
#import os
from os import path, chdir, remove, getcwd
import pandas as pd
import pickle
import sys, os
print(os.getcwd())
sys.path.append(os.path.realpath(os.path.dirname(__file__)+'/python'))
os.chdir('./python')
print(os.getcwd())
from python.modelManager import modelManager

if path.exists('./python/test/modelMasterTable.csv'):
    print('removing test modelMasterTable')
    remove('./python/test/modelMasterTable.csv')

class dummyModel():
    """set test input"""
    def __init__(self):
        self.model_metric = "{'metric' : 'auc'}"
        self.validation_data = [1, 2, 3, 4, 5, 6]
        self.model_object = 'your actual model goes here'

    def get_metric_score(self, data):
        print('test you get your model score with {}'.format(data))


class testlocalModelManeger():
    """Testing local modelManager checkin and checkout methods..."""
    def __init__(self, test_model):
        self.test_model = test_model
        self.run_save_model()

    def run_save_model():
        ModelManager = modelManager(
            model_object=dummyModel(),
            model_tag='test_model_tag',
            model_subtag='test_model_subtag',
            model_version='test_model_version',
            model_directory='./test/test_model_dir',
            config_path='./test',
            use_local='True')
        modelManager.checkin_model()

    def test_local_model_saving():
        print('test saving first model methods...')
        with open('./test/test_model_dir', "rb") as output_file:
            loaded_object = pickle.load(file=output_file)
        assert path.exists('./test/test_model_dir/model.pickle'), 'model.pkl does not exist...'
        assert type(loaded_object) is testModel, 'testmodel class incorrect...'

    def test_masterModelTable():
        print('testing masterModeTable creation and basic logic...')
        assert path.exists('./test/modelMasterTable.csv'), 'modelMasterTable does not exist...'
        masterTable = pd.read_csv('./test/modelMasterTable.csv', sep=';', index=False)
        assert masterTable.shape[0] == 1 & masterTable['deployment_status'][0] is True, 'masterModelTable content incorrect...'

    def test_local_save_more_file():
        # save second model
        self.run_save_model()
        print('test saving more files methods...')
        assert path.exists('./test/modelMasterTable.csv'), 'modelMasterTable does not exist...'
        masterTable = pd.read_csv('./test/modelMasterTable.csv', sep=';', index=False)
        assert masterTable.shape[0] == 2, 'masterModelTable row count incorrect...'
        assert masterTable['deployment_status'][0] is False & masterTable['decommission_date'][0] is not None, \
            'masterModelTable deactivation incorrect...'
        assert masterTable['deployment_status'][2] is True & masterTable['commission_date'][0] is not None, \
            'masterModelTable activation incorrect...'

    def test_local_load_file():
        print('testing loading files methods...')
        model = self.run_load_model()
        assert model.model_object is 'your actual model goes here', 'loading model incorrect...'
