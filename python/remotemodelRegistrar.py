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
from abc import ABC, abstractmethod

logging.basicConfig(format='%(asctime)s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',
    level=logging.INFO)
log = logging.getLogger('baseModelRegistrar')


class remoteModelRegistrar(baseModelRegistrar):

    "remote class to save and bookkeep deployable models across projects"

    def __init__(self, model_object, model_tag, model_subtag, model_version, 
                 s3_location, s3_bucket, s3_region): 
        # init base class
        baseModelRegistrar.__init__(self, model_object = model_subject, model_tag = model_tag, 
                                    model_subtag = model_subtag, model_version = model_version) 
        self.s3_location = s3_location
        self.s3_bucket = s3_bucket
        self.s3_region = s3_region

    def _define_model_path_info(self):
        model_path_item = {'
            'model_path': None, 
            's3_region': self.s3_region,
            's3_bucket': self.s3_bucket,
            's3_location': self.s3_location
        }
        return(model_path_item)

    def _get_model_path(self):
        #TODO: remote db setup
        log.error('To be implemented...')
        sys.exit(1)
        return(model_path)
    
    def _save_model_object(self):
        log.error('To be implemented as object put to s3')
        sys.exit(1)
        return
            
    def _save_modelMasterTemplate(self, masterTableSchema):
        log.error('To be implemented...')
        sys.exit(1)
        return

    def _load_masterModeltable(self):
        log.error('To be implemented...')
        sys.exit(1)
        return
  
    def _load_model_object(self):
        log.error('To be implemented...')
        sys.exit(1)
        return
    
    def _get_model_location(self):
        model_location = {
            s3_bucket = project_model['s3_bucket'],
            s3_location = project_model['s3_location'],
            s3_region = project_model['s3_region']
        } 
        return(model_location)
    
    def _load_model(self, file_path):
        log.error('To be implemented...')
        sys.exit(1)
        return#(model_object)
 
    


