# -*- coding: utf-8 -*-
# record model project, sub project, version, creation date,
# deployment_status, commission_date, decommission_date, metric

import logging
import os
import pandas as pd
import json
import csv
import pickle
import sys
from baseModelRegistrar import baseModelRegistrar
from utils.funcs import pickle_save_model, pickle_load_model, verify_and_create_dir
from abc import ABC, abstractmethod

logging.basicConfig(format='%(asctime)s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%d-%m-%Y:%H:%M:%S',
                    level=logging.INFO)
log = logging.getLogger('localModelRegistrar')


class localModelRegistrar(baseModelRegistrar):

    "local ModelRegistrar implementation for local model tracking..."

    def __init__(self, model_object, model_tag, model_subtag, model_version, model_directory,
                 masterModelTable_path='..'):
        log.info('Initializing localModelRegistrar class...')
        # init base class
        baseModelRegistrar.__init__(self, model_object=model_object, model_tag=model_tag,
                                    model_subtag=model_subtag, model_version=model_version)
        self.model_directory = model_directory
        self.masterModelTable_path = masterModelTable_path
        self.model_path = None

    def _define_model_path_info(self):
        self.model_path = self._get_model_path()
        log.info('Model path identified: {}...'.format(self.model_path))
        model_path_item = {
                            'model_path': self.model_path,
                            's3_region': None,
                            's3_bucket': None,
                            's3_location': None
        }
        return(model_path_item)

    def _get_model_path(self):
        model_path = self.model_directory + '/' + self.model_tag + '/' + self.model_subtag + '/' +\
                        self.model_version + '/'
        return(model_path)

    def _save_model_object(self):
        # # verify model path
        # verify_and_create_dir(self.model_directory)
        # verify model_object has proper attr and method
        self._check_model_object()
        # assume model_object has model_object, metric, validation_data attributes
        model_object = self.model_object.model_object
        # concat model file name
        log.info('Saving model_object: {} to local...'.format(self.model_path))
        pickle_save_model(model_object, self.model_path)
        log.info('Saved...')

    def _save_modelMasterTemplate(self, masterTableSchema):
        masterTableSchema_path = self.masterModelTable_path + '/masterModelTable.csv'
        masterTableSchema.to_csv(masterTableSchema_path, sep=';', index=False)
        log.info('modelMasterTemplate saved to local...')

    def _load_masterModeltable(self):
        model_file_path = self.masterModelTable_path + '/masterModelTable.csv'
        if not os.path.isfile(model_file_path):
            log.info("masterModeltable doesn't exist in {}, creating it now...".
                     format(model_file_path))
            masterModelTable = self._create_masterModelTable_schema()
        else:
            # to do: add masterTable repo path
            masterModelTable_path = self.masterModelTable_path+'/masterModelTable.csv'
            masterModelTable = pd.read_csv(masterModelTable_path, sep=';')
            log.info('masteModelTable retrieved from local...')
        return(masterModelTable)

    def _load_model_object(self):
        current_model_path = self.masterModelTable.query['model_id == {}'.
                                                         format(self.deployable_model_id)]['model_path']
        current_model_object = self._load_model(current_model_path)
        return(current_model_object)

    def _get_model_location(self, project_model_dataframe):
        model_location = {
            'model_path': project_model_dataframe.reset_index().loc[0, 'model_path']
        }
        return(model_location)

    def _load_model(self, file_path):
        model_object = pickle_load_model(file_path=file_path['model_path'])
        return(model_object)


print('Test your localModelRegistrar...')
