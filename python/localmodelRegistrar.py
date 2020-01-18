# -*- coding: utf-8 -*-
# record model project, sub project, version, creation date, 
# deployment_status, commission_date, decommission_date, metric 

import logging
import os
#import numpy as np
import pandas as pd
import json
import csv
import pickle
import sys
from abc import ABC, abstractmethod

logging.basicConfig(format='%(asctime)s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',
    level=logging.INFO)
log = logging.getLogger('baseModelRegistrar')


class localModelRegistrar(baseModelRegistrar):

    "local ModelRegistrar implementation for local model tracking..."

    def __init__(self, model_object, model_tag, model_subtag, model_version, model_directory): 
        # init base class
        baseModelRegistrar.__init__(self, model_object = model_subject, model_tag = model_tag, 
                                    model_subtag = model_subtag, model_version = model_version)
        self.model_directory = model_directory
        self.model_path = None   

    def _define_model_path_info(self):
        model_path_item = {'
            'model_path': self.model_path, 
            's3_region': None,
            's3_bucket': None,
            's3_location':None
        }
        return(model_path_item)

    def _get_model_path(self):
        model_path = self.model_directory + '/' + self.model_tag + '/' + self.model_subtag + '/' +\
                        self.model_version
        return(model_path)
    
    def _save_model_object(self):
        if not os.path.exists(self.model_directory):
            os.mkdir(self.model_directory)
        # assume model_object has model_object, metric, validation_data attributes
        model_object = self.model_object.get_value('model_object')
        # concat model file name
        log.info('Saving model_object: {} to local...'.format(self.model_path))
        pickle.dump(model_object, file = self.model_path)
        return
            
    def _save_modelMasterTemplate(self, masterTableSchema):
        modelMasterTemplate.write_csv('./masterModelTable.csv', sep = ';')
        log.info('modelMasterTemplate saved to local...')
        return

    def _load_masterModeltable(self):
        if os.path.isfile('modelModeltable.csv'):
            log.info("masterModeltable doesn't exist, creating it now...")
            self.masterModelTable = self._create_masterModelTable_schema()
        else: 
            self.masterModelTable = pd.read_csv('./masterModelTable.csv')
            log.info('masteModelTable retrieved from local...')
        # increment model_id
        self.model_id = self._find_model_id(masterModelTable = self.selfmasterModelTable)
        log.info('New model_id incremented...')

    def _load_model_object(self):
        current_model_path = self.masterModelTable.query['model_id == {}'.\
                        format(self.deployable_model_id)]['model_path']
        current_model_object = pickle.load(file = current_model_path)
        return(current_model_object)
    
    def _get_model_location(self):
        model_location = {
            model_path = project_model['model_path']
        } 
        return(model_location)

    def _load_model(self, file_path):
        model_file = open(file_path[self.model_path], 'rb')
        model_object = pickle.load(model_file)
        model_file.close()
        return(model_object)
 
