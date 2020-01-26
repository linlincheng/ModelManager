## ModelManager manages your model objects


### to save your model: 

You'll need to configure a model deployment logic in model_deployment.json for each model_tag, model_subtag pair. Please follow the format of examples given. At the moment, only 'latest' logic is implemented to help you keep track of your model traing history. 
Think of it as you legger. When the newest model with specified model_tag, model_subtag comes in, it deactivates the previous model with same specifics, and becomes the deployable model. In the meanwhile, you'll always be able to trace back to the previous models. 
Use model_version field in conjunction with detailed documentation on increments. 

initialize ModelManger class,

    ModelManager = modelManager.(
        model_object=test_model,
        model_tag='test_model_tag',
        model_subtag='test_model_subtag',
        model_version='test_model_version',
        model_directory='./test/test_model_dir',
        config_path='./test', 
        use_local=True)
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
        use_local=True)
    modelManager.chechout_model()
    model = modelManager.model_object


Note:

This is a WIP and many parts may be still under test and development. Currently only local versions work. More to come soon!


TODO:

1) fix test 

2) implement 'best_metric' loading method

3) update user manual

4) implement remote classes
