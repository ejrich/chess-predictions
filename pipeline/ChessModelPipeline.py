import sys, os
import numpy as np
import pandas as pd
from sklearn.externals import joblib
from sklearn.linear_model import SGDRegressor, SGDClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, log_loss, mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from CreateFeatureMatrices import create_feature_matrices

pieces = ['P', 'B', 'R', 'N', 'Q', 'K']
colors = ['1.0', '2.0']

def mapColumns(col_name, columns):
    return list(map(lambda x: col_name + '_' + x, columns)) 

def createLinearRegression(dataFrame, all_columns, dummy_columns):
    df_train, df_test = train_test_split(dataFrame)

    y_train = df_train["Result"].values
    y_test = df_test["Result"].values

    X_train, X_test = create_feature_matrices(df_train, df_test, all_columns, dummy_columns)

    all_lr = SGDRegressor(max_iter=2000)
    all_lr.fit(X_train, y_train)
    pred_result_all_test = all_lr.predict(X_test)
    all_mse = mean_squared_error(y_test, pred_result_all_test)
    all_rmse = np.sqrt(all_mse)

    print()
    print("All Columns Model MSE:", all_mse)
    print("All Columns Model RMSE:", all_rmse)

    return all_lr

def createLogisticRegression(dataFrame, all_columns, dummy_columns):
    df_train, df_test = train_test_split(dataFrame, stratify=dataFrame["Result"])

    encoder = LabelEncoder()
    y_train = encoder.fit_transform(df_train["Result"].astype("str"))
    y_test = encoder.transform(df_test["Result"].astype("str"))

    X_train, X_test = create_feature_matrices(df_train, df_test, all_columns, dummy_columns)
    
    all_lr = SGDClassifier(max_iter=2000, loss="log")
    all_lr.fit(X_train, y_train)
    pred_results = all_lr.predict(X_test)
    pred_prob = all_lr.predict_proba(X_test)

    accuracy = accuracy_score(y_test, pred_results)
    loss = log_loss(y_test, pred_prob)
    cm = confusion_matrix(y_test, pred_results)

    print()
    print("Model Accuracy:", accuracy)
    print("Loss:", loss)
    print("Labels:", encoder.classes_)
    print("Confusion matrix:")
    print(cm)

    return all_lr

def createModel(dataFile, modelFile):
    dataFrame = pd.read_csv(dataFile)

    numerical_columns = list(dataFrame.columns[1:-128])
    print(numerical_columns)

    categorical_columns = list(dataFrame.columns[-128:])
    print(categorical_columns)

    all_columns = numerical_columns + categorical_columns

    dummy_columns = {}
    for col_name in categorical_columns:
        dummies = pd.get_dummies(dataFrame[col_name], prefix=col_name)
        reindex_columns = mapColumns(col_name, pieces) if 'piece' in col_name else mapColumns(col_name, colors)
        dummies = dummies.reindex(columns=reindex_columns, fill_value=0)

        dummy_columns[col_name] = dummies.columns.values
        dataFrame = dataFrame.merge(dummies, left_index=True, right_index=True)
        dataFrame = dataFrame.drop(columns=col_name)
    
    # model = createLinearRegression(dataFrame, all_columns, dummy_columns)
    model = createLogisticRegression(dataFrame, all_columns, dummy_columns)

    joblib.dump(model, modelFile)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Please provide input and output files')
        exit(1)

    dataFile = os.path.join(os.path.dirname(__file__), sys.argv[1])
    modelFile = os.path.join(os.path.dirname(__file__), sys.argv[2])

    createModel(dataFile, modelFile)