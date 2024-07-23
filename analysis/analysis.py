import numpy as np
import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn import multioutput
from sklearn import metrics
from sklearn import linear_model
import joblib
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import RobustScaler
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import PolynomialFeatures
import math
import time
from sklearn.tree import DecisionTreeRegressor
import csv

#Current workflow:

# - Drop rows with -1s/static variables
# - Log1p (natural log, +1 to all before hand) - THIS WAS GOOD
# - MinMaxScaler (works better than Standard or Robust)
# - Train/Test split 80/20
# - SVR model, rbf kernel. Parameter tuned roughly by hand
# - Currently validating using root MSE to give "average" cycles away.

# Issues:

# - Missing lots of "outliers", starting to fit to trends better. Found more data = more outliers which seems good
# - Artificially bump up less represented groups (ie outliers) in data?
# - How is best to analyse/discuss? Anything else I need to consider or test?

curdir = "C:/Users/Joseph/Documents/simeng-parameter-study/analysis"
data = "aarch64-results.csv"
#data = "aarch64-results.csv"
MODEL_SAVE_NAME = "model.pkl"

data_path = os.path.join(curdir, data)
df = pd.read_csv(data_path)
print("Original df shape: ", df.shape)
#df = df[:20000]

config_options = ['Vector-Length','Streaming-Vector-Length','Fetch-Block-Size','Loop-Buffer-Size', \
                  'Loop-Detection-Threshold','Heap-Size','Stack-Size','GeneralPurpose-Count', \
                  'FloatingPoint/SVE-Count','Predicate-Count','Conditional-Count','Commit','FrontEnd', \
                  'LSQ-Completion','ROB','Load','Store','Access-Latency','Load-Bandwidth','Store-Bandwidth', \
                  'Permitted-Requests-Per-Cycle','Permitted-Loads-Per-Cycle','Permitted-Stores-Per-Cycle', \
                  'clw','core_clock','l1_latency','l1_clock','l1_associativity','l1_size','l2_latency', \
                  'l2_clock','l2_associativity','l2_size','ram_timing','ram_clock','ram_size']

#config_options = ['Vector-Length', 'Commit', 'ROB', 'l1_latency', 'l1_size', 'l2_latency', 'l2_size']
#config_options = ['Vector-Length', 'l1_latency']
#config_options = ['Vector-Length', 'ROB', 'l1_latency', 'l1_size', 'l2_latency', 'l2_size', "Load-Bandwidth", "Store-Bandwidth", "clw"]
#cycle_options = ['minibude_cycles', 'stream_cycles', 'tealeaf_cycles', 'cloverleaf_cycles', 'minisweep_cycles']
#cycle_options = ['minibude_cycles']
cycle_options = ['stream_cycles']

def clean_data(df):
    # Drop rows with -1 in cycle values
    dropped_rows = []
    for index, row in df.iterrows():
        for i in cycle_options:
            if row[i] == -1:
                dropped_rows.append(index)
    #for index, row in df.iterrows():
    #        if row["Vector-Length"] != 512:
    #            dropped_rows.append(index)
    df.drop(dropped_rows, inplace=True)

    # Exclude unchanged values, and update the config list to show this
    unchanged_options = ['Streaming-Vector-Length', 'Heap-Size', 'Stack-Size', 'Access-Latency', \
                         'core_clock', 'ram_size']
    df.drop(columns=unchanged_options, inplace=True)
    for i in unchanged_options:
        if i in config_options:
            config_options.remove(i)

    return df

def get_data_stats(df):
    for column in df.columns:
        mean_value = df[column].mean()
        std_value = df[column].std()
        min_value = df[column].min()
        max_value = df[column].max()
        median_value = df[column].median()

        print(f"Statistics for column '{column}':")
        print(f"  Mean: {mean_value}")
        print(f"  Std Dev: {std_value}")
        print(f"  Min: {min_value}")
        print(f"  Max: {max_value}")
        print(f"  Median: {median_value}")

def save_model(model):
    joblib.dump(model, MODEL_SAVE_NAME)
    print("Saved model to " + MODEL_SAVE_NAME)

def load_model(save_name):
    model = joblib.load(save_name)
    print("Loaded model from " + save_name)
    return model

def save_sample(num_samples):
    X_test_subset = X_test[:num_samples]
    Y_test_subset = Y_test[:num_samples]
    Y_pred_subset = Y_pred[:num_samples]
    X_test_df = pd.DataFrame(X_test_subset, columns=df_config.columns)
    Y_test_df = pd.DataFrame(Y_test_subset, columns=df_cycles.columns)
    Y_pred_df = pd.DataFrame(Y_pred_subset, columns=df_cycles.columns)
    Y_pred_columns = {col: f"{col}_pred" for col in df_cycles.columns}
    Y_test_columns = {col: f"{col}_actual" for col in df_cycles.columns}
    Y_pred_df.rename(columns=Y_pred_columns, inplace=True)
    Y_test_df.rename(columns=Y_test_columns, inplace=True)
    results_df = pd.concat([X_test_df, Y_pred_df, Y_test_df], axis=1)
    results_df.to_csv('test_predictions.csv', index=False)

def single_model():
    print(Y_train.shape, Y_test.shape)
    model.fit(X_train, Y_train)
    return model

def multi_model():
    multi_output_model = multioutput.MultiOutputRegressor(model, n_jobs=-1)
    multi_output_model.fit(X_train, Y_train)
    return multi_output_model


def grid_search():
    param_grid = {
    'estimator__C': [0.1, 1, 10],
    #'estimator__epsilon': [0.1, 0.2, 0.5],
    'estimator__epsilon': [0.2],
    'estimator__kernel': ['poly', 'rbf'],
    }
    multi_output_svm = multioutput.MultiOutputRegressor(model, n_jobs=-1)
    grid_search = GridSearchCV(multi_output_svm, param_grid, cv=5, scoring='neg_mean_squared_error', n_jobs=-1)
    grid_search.fit(X_train, Y_train)
    for mean_score, params in zip(grid_search.cv_results_['mean_test_score'], grid_search.cv_results_['params']):
        print(f"Mean Score: {mean_score}, Params: {params}")
    best_svm = grid_search.best_estimator_
    # Predict on the test set
    Y_pred = best_svm.predict(X_test)

    # Evaluate the model
    mse = metrics.mean_squared_error(Y_test, Y_pred, multioutput='raw_values')
    print("Mean Squared Error for each target:", mse)

def compare_graph(config_option, cycle_option):
    plt.figure(figsize=(10, 6))
    #plt.scatter(df_config[config_option], df_cycles[cycle_option], alpha=0.5)
    plt.scatter(X_test[config_option], Y_test[cycle_option], alpha=0.5)
    plt.scatter(X_test[config_option], Y_pred[cycle_option], alpha=0.5, color="red")
    plt.title(config_option + " vs " + cycle_option)
    plt.xlabel(config_option)
    plt.ylabel(cycle_option)
    plt.grid(True)


df = clean_data(df)
total_results = []
result_cols = config_options + ["perc_acc", "one_perc", "two_perc", "five_perc", "ten_perc"]

for current_code in cycle_options:
    start_time = time.time()
    print("df shape after data cleaning: ", df.shape)

    df_config = df[config_options].copy()
    df_cycles = df[[current_code]].copy()

    print("df_config shape:", df_config.shape)
    print("df_cycles shape:", df_cycles.shape)
    #get_data_stats(df_cycles)

    X = df_config.values
    Y = df_cycles.values
    #Y = np.log1p(Y)
    #poly = PolynomialFeatures(degree=2, include_bias=False)
    #X_poly = poly.fit_transform(X)

    scaled_X = MinMaxScaler()
    #scaled_X = RobustScaler()
    #scaled_X = StandardScaler()
    X_scaled = scaled_X.fit_transform(X)

    scaled_Y = MinMaxScaler()
    #scaled_Y = RobustScaler()
    #scaled_Y = StandardScaler()
    Y_scaled = scaled_Y.fit_transform(Y)

    X_train, X_test, Y_train, Y_test = train_test_split(X_scaled, Y_scaled, test_size=0.2, random_state=42)

    end_time = time.time()
    print("Data prep took ", end_time - start_time, "s")

    start_time = time.time()
    #model = svm.SVR(verbose=0, cache_size=32000, kernel='rbf', C=5, epsilon=0.001)
    model = DecisionTreeRegressor(random_state=0)
    #model = linear_model.Lasso()
    #model = linear_model.LinearRegression(positive=True)
    #model = linear_model.Ridge()
    #C=10, epsilon=0.2


    LOAD_SAVE = False
    SAVE_MODEL = False

    if (LOAD_SAVE):
        model = load_model(MODEL_SAVE_NAME)
    else:
        #model = single_model()
        model.fit(X_train, Y_train)
        if (SAVE_MODEL):
            save_model(model)


    #model = multi_model()
    #model = single_model()
    #grid_search()

    Y_pred_scaled = model.predict(X_test).reshape(-1, 1)
    print("Predicted Y")
    X_test = scaled_X.inverse_transform(X_test)
    Y_test = scaled_Y.inverse_transform(Y_test)
    Y_pred = scaled_Y.inverse_transform(Y_pred_scaled)
    #Y_pred = np.expm1(Y_pred)
    #Y_test = np.expm1(Y_test)

    Y_pred_df = pd.DataFrame(Y_pred, columns=df_cycles.columns)
    get_data_stats(Y_pred_df)
    end_time = time.time()
    print("Model training took ", end_time - start_time, "s")


    #X_test = pd.DataFrame(X_test, columns=df_config.columns)
    #Y_test = pd.DataFrame(Y_test, columns=df_cycles.columns)
    #Y_pred = pd.DataFrame(Y_pred, columns=df_cycles.columns)
    #for i in config_options:
    #    compare_graph(i, "stream_cycles")

    #boxplot_df = pd.concat([df_config["l1_latency"], df_cycles["minibude_cycles"]], axis=1)
    #sns.boxplot(data=boxplot_df, x="l1_latency", y="minibude_cycles")

    plt.show()

    #mse = metrics.mean_squared_error(Y_test, Y_pred)
    #print("Mean Squared Error for each target:", mse)
    #target_mse = 100000*100000
    #print("Target MSE is ", target_mse, " which is average 100k cycles away.")
    #print("Achieved sqrt MSE is ", math.sqrt(mse), " cycles away" )

    results = []

    feature_importances = model.feature_importances_
    for i in range(len(feature_importances)):
        results.append(feature_importances[i]*100)
        print(config_options[i], ": ", feature_importances[i]*100, "%")

    #test = results_table["minibude_cycles"]
    total_pred = len(Y_pred)
    limit_perc = 2
    perc_results = []

    #Get mean % accuracy
    total_diff = 0
    for i in range(len(Y_pred)):
        total_diff += abs(1 - (Y_pred[i]/Y_test[i]))
    results.append(float(100 - (total_diff / len(Y_pred)) * 100))

    #Get percentage that fall under several percent boundaries
    for limit_perc in [1, 2, 5, 10]:
        counter = 0
        for i in range(len(Y_pred)):
            if abs(((Y_pred[i] / Y_test[i]) - 1) * 100) < limit_perc:
                counter += 1
        results.append((counter/total_pred)*100)
        print(counter, " out of ", total_pred, " predictions were within ", limit_perc, "%. That is ", (counter/total_pred)*100, "%")

    total_results.append(results)

    
#print(total_results)

#results_df = pd.DataFrame(columns=result_cols)
#for i in total_results:
#    results_df.loc[len(results_df), :] = i
#results_df.to_csv("model_results.csv")

#print(results_table)

save_sample(200)


