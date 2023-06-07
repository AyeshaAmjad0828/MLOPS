# train.py
from flaml import AutoML
from flaml.data import get_output_from_log
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import pymongo
from pymongo import MongoClient
import pandas as pd
import pickle
import json
import numpy as np



#fetch mongo db parameters from the json file
with open("C:/Users/ayesha.amjad/Documents/GitHub/BigDataProject/MLOPS/Project/webpage/mongo_params.json", "r") as json_file:
    mongo_params = json.load(json_file)

# Connect to the MongoDB container
mongo_uri = mongo_params["Client"]
database_name = mongo_params["db"]
collection_name = mongo_params["collection"]

client = MongoClient(mongo_uri)
db = client[database_name]
collection = db[collection_name]
cursor = collection.find()
data = list(cursor)
df = pd.DataFrame(data)

# Connect to the MongoDB container
#client = MongoClient('mongodb://localhost:27017')
#db = client['Customers']
#collection = db['ChurnData']
#cursor = collection.find()
#data = list(cursor)
#df = pd.DataFrame(data)



#identify and drop contant value columns
constant_columns = [col for col in df.columns if df[col].nunique() == 1]
df = df.drop(constant_columns, axis=1)


#identify and drop sequential columns
sequential_columns = []
for col in df.columns:
    if df[col].dtype in [np.int64, np.int32, np.float64]:
        differences = np.diff(df[col])
        if np.all(differences == differences[0]):
            sequential_columns.append(col)

df = df.drop(sequential_columns, axis=1)
df = df.drop('_id', axis=1)



#deal with missing values
df = df.replace(r'^\s*$', pd.NA, regex=True)

#identify numeric and categorical variables
numeric_cols = df.select_dtypes(include=np.number).columns
categorical_cols = df.select_dtypes(include=np.object).columns

# Mean imputation for numeric fields and Mode imputation for categorical fields
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
df[categorical_cols] = df[categorical_cols].fillna(df[categorical_cols].mode().iloc[0])



#fetch automl parameters from the json file
with open("C:/Users/ayesha.amjad/Documents/GitHub/BigDataProject/MLOPS/Project/webpage/automl_params.json", "r") as json_file:
    automl_params = json.load(json_file)


#X,y
target_col = automl_params["target"]
X=df.drop(columns=[target_col])
y=df[target_col]
y

#Test train split
split_percentage = int(automl_params["test_size"])/100
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=split_percentage, random_state=42)

#encoding and pre-processing
le = LabelEncoder()
for column in X.columns:
    if X[column].dtype == object:
        X[column] = le.fit_transform(X[column])


#set evaluation metrics as per different tasks and automl settings
task = automl_params["task"].lower()
if task == 'classification':
    metric = 'roc_auc'
else:
    metric = 'r2'


automl = AutoML()   
automl_settings = {
    "time_budget": 60,
    "metric": metric,
    "task": automl_params["task"].lower(),
    "log_file_name": 'automl.log',
    "model_history": True,
}


# Train the model using the data
automl.fit(X_train=X_train, y_train=y_train, dataframe=data, **automl_settings)

# Save the best model for deployment
best_model = automl.model
print(best_model)




def map_values_to_columns(array, dataframe):
    column_names = dataframe.columns.tolist()
    result = {}
    for i in range(len(column_names)):
        result[column_names[i]] = array[i]
    return result

feature_imp = map_values_to_columns(automl.feature_importances_, X_train)
feature_imp =pd.DataFrame(feature_imp, index=[1])

t_feature_imp = feature_imp.transpose().reset_index()
t_feature_imp.columns = ['Feature', 'Importance']
t_feature_imp.to_csv('C:/Users/ayesha.amjad/Documents/GitHub/BigDataProject/MLOPS/Project/featureImp.csv', sep=',', index=False)


'''retrieve best config and best learner'''
best_learner = automl.best_estimator
learning_rate = automl.best_config["learning_rate"]
accuracy = 1-automl.best_loss
best_time = automl.best_config_train_time

best_metrics = {
    "accuracy": accuracy,
    "best_learner": best_learner,
    "best_time": best_time,
    "learning_rate": learning_rate,
}
with open("C:/Users/ayesha.amjad/Documents/GitHub/BigDataProject/MLOPS/Project/best_metrics.json", 'w') as json_file:
    json.dump(best_metrics, json_file)


#getting loss and time values from log file

from flaml.data import get_output_from_log
time_history, best_valid_loss_history, valid_loss_history, config_history, metric_history = \
    get_output_from_log(filename=automl_settings['log_file_name'], time_budget=240)
for config in config_history:
    print(config)

timehist = pd.DataFrame(time_history, columns=['time history'])
losshist = pd.DataFrame(1 - np.array(valid_loss_history), columns=['valid loss'])
bestlosshist = pd.DataFrame(1 - np.array(best_valid_loss_history), columns=['best valid loss'])
scatter_data = pd.concat([timehist, losshist, bestlosshist], axis=1)
scatter_data.to_csv('C:/Users/ayesha.amjad/Documents/GitHub/BigDataProject/MLOPS/Project/LossMetrics.csv', sep=',', index=False)


#Save best performing model graph
## plt.title('Learning Curve')
## plt.xlabel('Wall Clock Time (s)')
## plt.ylabel('Validation Accuracy')
## plt.scatter(time_history, 1 - np.array(valid_loss_history))
# #plt.step(time_history, 1 - np.array(best_valid_loss_history), where='post')


# Save the best model to a file or cloud storage for later use
model_path =r'C:\Users\ayesha.amjad\Documents\GitHub\BigDataProject\MLOPS\Project\model\bestmodel.pkl'

with open(model_path, 'wb') as file:
    pickle.dump(best_model, file)

