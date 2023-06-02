# train.py
from flaml import AutoML
from flaml.data import get_output_from_log
from pymongo import MongoClient
import pymongo
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend
import matplotlib.pyplot as plt
import numpy as np

# Connect to the MongoDB container
client = MongoClient('mongodb://localhost:27017')
db = client['Customers']
collection = db['ChurnData']
cursor = collection.find()
data = list(cursor)
df = pd.DataFrame(data)

#data = list(collection.find({}, {'_id': 0}))
df = df.drop('_id', axis=1)
df = df.drop(columns=['RowNumber', 'CustomerId', 'Surname'], axis=1)

#X,y
target_col = 'Exited'
X=df.drop(columns=[target_col])
y=df[target_col]
y

# Perform necessary preprocessing on the data
automl = AutoML()
automl_settings = {
    "time_budget": 200,
    "metric": 'roc_auc',
    "task": 'classification',
    "log_file_name": 'automl.log',
    "model_history": True,
}


# Train the model using the data
automl.fit(X_train=X, y_train=y, dataframe=data, **automl_settings)

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


from flaml.data import get_output_from_log
time_history, best_valid_loss_history, valid_loss_history, config_history, metric_history = \
    get_output_from_log(filename=automl_settings['log_file_name'], time_budget=240)
for config in config_history:
    print(config)



plt.title('Learning Curve')
plt.xlabel('Wall Clock Time (s)')
plt.ylabel('Validation Accuracy')
plt.scatter(time_history, 1 - np.array(valid_loss_history))
plt.step(time_history, 1 - np.array(best_valid_loss_history), where='post')
plt.show()
plt.savefig(r'C:\Users\ayesha.amjad\Documents\GitHub\BigDataProject\MLOPS\Project\model\roc_auc_curve.png')  

import pickle
# Save the best model to a file or cloud storage for later use


model_path =r'C:\Users\ayesha.amjad\Documents\GitHub\BigDataProject\MLOPS\Project\model\bestmodel.pkl'

with open(model_path, 'wb') as file:
    pickle.dump(best_model, file)

#best_model.save_model('/app/best_model')
