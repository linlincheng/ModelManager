# -*- coding: utf-8 -*-
# record model project, sub project, version, creation date,
# deployment_status, commission_date, decommission_date, metric

import logging
from abc import ABC, abstractmethod

logging.basicConfig(format='%(asctime)s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%d-%m-%Y:%H:%M:%S',
                    level=logging.INFO)
log = logging.getLogger('baseFramework')


class baseFramework(object):
    "base class to unify model inteface for local and remote scenarios"

    def __init__(self, model_object, model_tag, model_subtag, model_version):
        log.info('Initializing baseFramework class...')
        # def common attributes
        self.model_object = model_object
        self.model_tag = model_tag
        self.model_subtag = model_subtag
        self.model_version = model_version

    @abstractmethod
    # def public method: save_model interface
    def save_model(self):
        return

    @abstractmethod
    # def public method: load_deployable interface
    def load_deployable_model(self):
        return


print('Test your print...')
