# Testing local io using mock
# test/model_deployment.json and test/.modelMasterTable.csv
from os import path, chdir, remove, getcwd
import pandas as pd
import pickle
import sys
from python.modelManager import modelManager

if path.exists('./test/masterModelTable.csv'):
    print('removing test masterModelTable')
    remove('./test/masterModelTable.csv')


class dummyModel():
    """set test input"""
    def __init__(self):
        self.model_metric = "{'metric' : 'auc'}"
        self.validation_data = [1, 2, 3, 4, 5, 6]
        self.model_object = 'your actual model goes here'

    def get_metric_score(self, data):
        print('test you get your model score with {}'.format(data))


class TestlocalModelManeger():
    """Testing local modelManager checkin and checkout methods..."""

    def run_save_model(self):
        ModelManager = modelManager(
            model_object=dummyModel(),
            model_tag='test_model_tag',
            model_subtag='test_model_subtag',
            model_version='test_model_version',
            model_directory='./test/test_model_dir',
            config_path='./test',
            use_local='True')
        ModelManager.checkin_model()

    def run_load_model(self):
        ModelManager = modelManager(
            model_tag='test_model_tag',
            model_subtag='test_model_subtag',
            model_version='test_model_version',
            model_directory='./test/test_model_dir',
            config_path='./test',
            use_local='True')
        ModelManager.checkout_model()
        return(ModelManager.model_object)

    def test_local_model_saving(self):
        # run save_model first
        self.run_save_model()
        print('test saving first model methods...')
        model_path = './test/test_model_dir/test_model_tag/test_model_subtag/test_model_version'
        file_path = model_path + '/model.pickle'
        assert path.exists(file_path), 'model.pkl does not exist...'
        with open(file_path, "rb") as output_file:
            loaded_object = pickle.load(file=output_file)
        assert isinstance(loaded_object, str), 'testmodel class incorrect...'

    def test_masterModelTable(self):
        print('testing masterModeTable creation and basic logic...')
        assert path.exists('./test/masterModelTable.csv'), 'masterModelTable does not exist...'
        masterTable = pd.read_csv('./test/masterModelTable.csv', sep=';')
        assert masterTable.shape[0] == 1, 'masterModelTable shape incorrect...'
        assert masterTable['deployment_status'][0], 'masterModelTable deployment_status incorrect...'

    def test_local_save_more_file(self):
        # save second model
        self.run_save_model()
        print('test saving more files methods...')
        assert path.exists('./test/masterModelTable.csv'), 'masterModelTable does not exist...'
        masterTable = pd.read_csv('./test/masterModelTable.csv', sep=';')
        assert masterTable.shape[0] == 2, 'masterModelTable row count incorrect...'
        assert not masterTable['deployment_status'][0], \
            'masterModelTable deactivation incorrect...'
        assert masterTable['deployment_status'][1], \
            'masterModelTable activation incorrect...'

    def test_local_load_file(self):
        print('testing loading files methods...')
        model = self.run_load_model()
        assert model == 'your actual model goes here', 'loading model incorrect...'
