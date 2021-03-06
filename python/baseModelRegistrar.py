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
from python.utils.funcs import get_current_datetime
from abc import ABC, abstractmethod
from python.baseFramework import baseFramework

logging.basicConfig(format='%(asctime)s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%d-%m-%Y:%H:%M:%S',
                    level=logging.INFO)
log = logging.getLogger('baseModelRegistrar')


class baseModelRegistrar(baseFramework):

    "base Regitrar class with common implementation for local and remote scenarios"

    def __init__(self, model_object, model_tag, model_subtag, model_version):  # not use_local,  model_directory and s3 related
        # init base class
        log.info('Initializing baseModelRegistrar class...')
        baseFramework.__init__(self, model_object=model_object, model_tag=model_tag,
                               model_subtag=model_subtag, model_version=model_version)
        self.model_id = None
        self.masterModelTable = None
        self.new_model_entry = None
        self.deployable_model_id = None
        self.current_datetime = get_current_datetime()

    def _save_masterModelTable(self):
        # by default, model gets saved to project/model directory
        self.masterModelTable = self._load_masterModeltable()
        # create local copy
        masterModelTable = self.masterModelTable
        # check deployment status
        # add deployment fields: deployment status, commission_date, decommision_date
        deployment_entry = self._check_model_deployment_logic()
        # get basic modelMaster meta info
        new_model_base_info = self._set_up_base_modelMasterTable_info()
        # append to masterModelTable
        self.new_model_entry = dict(deployment_entry, **new_model_base_info)
        # update masterModelTable
        self.masterModelTable = masterModelTable.append(self.new_model_entry, ignore_index=True)
        # save updated masterModelTabel
        self._save_modelMasterTemplate(self.masterModelTable)

    def save_model(self):
        # check model_object attributes, get_metric_score
        self._check_model_object()
        # save updated masterModelTabel
        self._save_masterModelTable()
        # save model object
        self._save_model_object()

    def _set_up_base_modelMasterTable_info(self):
        # set up schema
        new_model_base_info = {
            "model_id": self._find_model_id(self.masterModelTable),
            "model_tag": self.model_tag,
            "model_subtag": self.model_subtag,
            "model_version": self.model_version,
            "model_metric ": self.model_object.model_metric,
            "creation_date": self.current_datetime['current_time'],
        }
        model_path_item = self._define_model_path_info()
        new_model_base_info = dict(model_path_item, **new_model_base_info)
        return(new_model_base_info)

    @abstractmethod
    def _define_model_path_info(self):
        log.info('need to implement for local and remote...')
        raise NotImplementedError
        pass

    @abstractmethod
    def _save_model_object(self):
        log.info('need to implement for local and remote...')
        raise NotImplementedError
        pass

    def _create_masterModelTable_schema(self):
        log.info('Creating new masterModelTable')
        column_names = ['model_id', 'model_tag', 'model_subtag', 'model_path', 'model_version',
                        's3_region', 's3_bucket', 's3_location',
                        # TODO: check where it's been duped: model_metric','commision_date',
                        'deployment_status', 'creation_date', 'decommission_date']
        modelMasterTemplate = pd.DataFrame(columns=column_names)
        return(modelMasterTemplate)

    @abstractmethod
    def _save_modelMasterTemplate(self, masterTableSchema):
        log.info('need to implement for local and remote...')
        raise NotImplementedError
        pass

    @abstractmethod
    def _load_masterModeltable(self):
        log.info('need to implement for local and remote...')
        raise NotImplementedError
        pass

    def _find_model_id(self, masterModelTable):
        if masterModelTable is None or masterModelTable.shape[0] < 1:
            model_id = 0
        else:
            model_id = max(masterModelTable['model_id'])+1
        return(model_id)

    def _parse_model_deployment_logic(self, model_deployment_json='./model_deployment.json'):
        if not os.path.exists('model_deployment_logic.json not set up, \
                               use "latest" as default logic....'):
            model_deployment_logic = 'latest'
        else:
            deployment_json = []
            with open(model_deployment_json) as json_file:
                deployment_json = json.load(json_file, object_pairs_hook=OrderedDict)
            model_deployment_entry = deployment_json.get_value(self.model_tag, None).get_value(self.model_subtag, None)
            if model_deployment_entry is not None:
                model_deployment_logic = model_deployment_entry.get_value('deployment_logic')
            log.info('Model_deployment found: {}'.format(model_deployment_logic))
        return(model_deployment_logic)

    def _check_model_deployment_logic(self):
        # TODO: set up deployment json for each model_tag, model_subtag pair,
        # by default deploy the latest: overwrite previous deployable entry
        # check deployment_logic from config
        deployment_logic = self._parse_model_deployment_logic()
        # set up entry in masterModelTable
        if deployment_logic is 'latest':
            if self.masterModelTable.shape[0] < 1:
                log.info('No model_tag, model_subtag found in existing modelMasterTable, \
                    set as new pair...')
                deployment_entry = self._set_deployment_entry()
            else:
                result_dict = self._update_current_masterModelTable()
                self.masterModelTable = result_dict['masterModelTable']
                deployment_entry = result_dict['deployment_entry']
        elif deployment_logic is 'best_metric':
            deployment_entry = self._check_best_metric_deployment_status(metric=deployment_logic)
        self.masterModelTable.append(deployment_entry, ignore_index=True)
        log.info('masterModelTable updated, returning deployment entry...')
        return(deployment_entry)

    def _set_deployment_entry(self, update=True):
        if update:
            deployment_entry = {
                        'deployment_status': True,
                        'commission_date': self.current_datetime['current_time'],
                        'decommission_date': None
                    }
        else:
            deployment_entry = {
                        'deployment_status': False,
                        'commission_date': None,
                        'decommission_date': None
            }
        return(deployment_entry)

    def _retrive_deployable_model_info(self):
        deployable_model_info = self.masterModelTable.query('model_tag == "{model_tag}" & model_subtag == "{model_subtag}" & \
                                                           model_version == "{model_version}" & \
                                                           deployment_status == True'.format(
                                                        model_tag=self.model_tag,
                                                        model_subtag=self.model_subtag,
                                                        model_version=self.model_version))
        deployable_number = deployable_model_info.shape[0]
        log.info('Found current deployable model_id row count: {}'.format(deployable_number))
        if deployable_number != 1:
            log.error('Found {} deployable models for model_tag, model subtag pair...'.format(deployable_number))
            sys.exit(1)
        return(deployable_model_info)

    def _update_current_masterModelTable(self):
        log.info('Updating current masterModeTable information...')
        deployable_model_info = self._retrive_deployable_model_info()
        self.deployable_model_id = deployable_model_info['model_id']
        masterModelTable = self.masterModelTable
        log.info('Overwriting previous deployable model status to False...')
        decomission_update = pd.Series(data=['False', self.current_datetime['current_time']],
                                       index=['deployment_status', 'decommission_date'])
        masterModelTable.loc[int(self.deployable_model_id), decomission_update.index] = decomission_update
        return({'masterModelTable': masterModelTable,
                'deployment_entry': self._set_deployment_entry()})

    def _check_best_metric_deployment_status(self, metric):
        # assume best metric field consists of json string format: e.g. {'auc': 0.89}
        # to do: need to error handling no metric found default to first one
        # steps: 1) retrive current active model location
        current_model_object = self._load_model_object()
        # steps: 2) score using self.model_object.get_value('validation_data')
        current_model_inference = current_model_object.get_inference(data_frame=self.model_object.
                                                                     get_value('validation_data'))
        current_model_score = current_model_inference.get_metric_score(metric)
        # TODO: if metric does exit, raise error
        # steps: 3) compare score
        if current_model_score >= self.model_object.get_value('metric').get_value(metric):
            # do not update existing modelMasterTable, set current entry to False
            log.info('current_deployable_model_score is greater than latest, \
                      do not deploy new model...')
            deployment_entry = self._set_deployment_entry(update=False)
        else:
            log.info('latest model_score is greater than curent_deployabled_model_score, \
                      deploy new model...')
            # update current masterModelTable
            result_dict = self._update_current_masterModelTable()
            self.masterModelTable = result_dict['masterModelTable']
        # steps: 4) deployment_entry
            deployment_entry = result_dict['deployment_entry']
        return(deployment_entry)

    @abstractmethod
    def _load_model_object(self):
        log.info('need to implement for local and remote...')
        raise NotImplementedError
        pass

    def _check_model_object(self):
        # check model_object has proper method setup
        self._check_model_object_method()
        # check model_object has proper attribute setup
        attr_list = ['validation_data', 'model_metric', 'model_object']
        [self._check_model_object_attr(attr) for attr in attr_list]

    def _check_model_object_method(self):
        log.info('Checking model object has get_metric_score method implemented...')
        assert callable(self.model_object.get_metric_score), \
            'model_object needs get_metric_score method to proceed, please implement it...'
        return

    def _check_model_object_attr(self, attr):
        log.info('Checking model object has {} attribute...'.format(attr))
        assert hasattr(self.model_object, attr), \
            'model_object needs {} to proceed, please verify...'.format(attr)
        return

    def _check_deployable_model_location(self):
        if self.masterModelTable.shape[0] < 1:
            log.error('masterModelTable not found, save the model to your masterModelTable location first')
            raise IOError
        else:
            project_model_dataframe = self.masterModelTable.query('model_tag == "{model_tag}" & model_version == "{model_version}" &\
                model_subtag == "{model_subtag}" & deployment_status == True'.format(model_tag=self.model_tag,
                                                                                     model_subtag=self.model_subtag,
                                                                                     model_version=self.model_version))
        if project_model_dataframe.shape[0] != 1:
            log.error('model_tag, model_subtag info found {} pair(s) in masterModelTable, please \
                        check entries...'.format(project_model_dataframe.shape[0]))
            sys.exit(1)
        else:
            model_location = self._get_model_location(project_model_dataframe)
            return(model_location)

    @abstractmethod
    def _get_model_location(self):
        # return  # (model_location)
        log.info('need to implement for local and remote...')
        raise NotImplementedError
        pass

    @abstractmethod
    def _load_model(self, file_path):
        log.info('need to implement for local and remote...')
        raise NotImplementedError
        pass

    # callable public mehtod: run load_deployable_model for inference jobs
    def load_deployable_model(self):
        # load masterModelTable
        self.masterModelTable = self._load_masterModeltable()
        # check location
        model_location = self._check_deployable_model_location()
        # load_model object
        model_object = self._load_model(file_path=model_location)
        return(model_object)


print('Test your baseModelRegistrar...')
