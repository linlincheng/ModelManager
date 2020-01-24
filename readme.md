## ModelManager manages your model objects


### to save your model: 

initialize ModelManger class,

    ModelManager = modelManager.(
        model_object=test_model,
        model_tag='test_model_tag',
        model_subtag='test_model_subtag',
        model_version='test_model_version',
        model_directory='./test/test_model_dir',
        config_path='./test', 
        use_local = True)
    modelManager.checkin_model()


You'll be able to save your model objects to your specifed path and create a csv file to track model persistency meta info.

### to load your saved model:

    ModelManager = modelManager.(
        model_object=None,
        model_tag='test_model_tag',
        model_subtag='test_model_subtag',
        model_version='test_model_version',
        model_directory='./test/test_model_dir',
        config_path='./test', 
        use_local = True)
    model = modelManager.chechout_model()


Note:

This is a WIP and many parts may be still under test and development. Currently only local versions work. More to come soon!
