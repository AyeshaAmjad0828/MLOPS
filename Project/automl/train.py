# train.py
from flaml import AutoML
from flaml.data import get_output_from_log
from pymongo import MongoClient

# Connect to the MongoDB container
client = MongoClient('mongodb://mongodb:27017')
db = client['mydb']
collection = db['mycollection']

# Fetch data from the MongoDB collection
data = list(collection.find({}, {'_id': 0}))


#train/test split


# Perform necessary preprocessing on the data

automl = AutoML()
automl_settings = {
    "time_budget": 200,
    "metric": 'roc_auc',
    "task": 'classification',
    "log_file_name": 'automl.log',
    "model_history": True,
}

# Define your AutoML model
automl = AutoML()

# Train the model using the data
automl.fit(X_train=X_train, y_train=y_train, dataframe=data, **automl_settings)

# Save the best model for deploymen
best_model = automl.model
best_score = automl.best_loss
print(best_model)
print(best_score)


'''retrieve best config and best learner'''
print('Best ML leaner:', automl.best_estimator)
print('Best hyperparmeter config:', automl.best_config)
print('Best accuracy on validation data: {0:.4g}'.format(1-automl.best_loss))
print('Training duration of best run: {0:.4g} s'.format(automl.best_config_train_time))

# Save the best model to a file or cloud storage for later use
best_model.save_model('/app/best_model')
