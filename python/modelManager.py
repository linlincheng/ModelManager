from python.baseModelRegistrar import baseModelRegistrar
from python.localmodelRegistrar import localModelRegistrar
import logging

logging.basicConfig(
    format='%(asctime)s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',
    level=logging.INFO
 )
log = logging.getLogger('ModelManager')


class modelManager():
    """Your wrapper class to interact with local and remote io options"""

    def __init__(self, model_tag, model_subtag, model_version, model_object=None, use_local=True,
                 model_directory=None, masterModelTable_path='..', s3_location=None,
                 s3_bucket=None, s3_region=None, config_path=None):
        # check param config
        if use_local:
            local_list = [model_directory, config_path]
            assert None not in local_list, 'model_directory must be set for local io...'
            self.model_directory = model_directory
        else:
            remote_list = [s3_location, s3_bucket, s3_region]
            assert None not in [remote_list], 's3 configurations must be set for remote io...'
            self.s3_bucket = s3_region
            self.s3_region = s3_region
            self.s3_location = s3_location
        self.model_object = model_object
        self.model_tag = model_tag
        self.model_subtag = model_subtag
        self.model_version = model_version
        self.use_local = use_local
        self.config_path = config_path

    def checkin_model(self):
        """loads model from your set up"""
        log.info("Checking in your model object...")
        if self.use_local:
            self._save_local_model()
        else:
            self._save_remote_model()

    def checkout_model(self):
        log.info("Checking out your model object...")
        if self.use_local:
            self._load_local_model()
        else:
            self._load_remote_model()

    def _save_local_model(self):
        """saves model according to your set up"""
        localRegistrar = localModelRegistrar(
            model_object=self.model_object,
            model_tag=self.model_tag,
            model_subtag=self.model_subtag,
            model_version=self.model_version,
            model_directory=self.model_directory,
            config_path=self.config_path
        )
        localRegistrar.save_model()
        log.info('Model object saved...')

    def _load_local_model(self):
        localRegistrar = localModelRegistrar(
            model_object=self.model_object,
            model_tag=self.model_tag,
            model_subtag=self.model_subtag,
            model_version=self.model_version,
            model_directory=self.model_directory,
            config_path=self.config_path)
        self.model_object = localRegistrar.load_deployable_model()
        log.info('Model object loaded...')
        print(type(self.model_object))
        return(self.model_object)

    def _save_remote_model(self):
        log.error('To be implemented...')
        pass

    def _load_remote_model(self):
        log.error('To be implemented...')
        pass
