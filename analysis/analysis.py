import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn import multioutput
from sklearn import metrics
import joblib
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt
import time
from sklearn.tree import DecisionTreeRegressor
from sklearn.inspection import permutation_importance


#Specify the directory of this file
curdir = "~/path/to/cur/dir"
#Specify the name of the input data csv file
data = "aarch64-results.csv"

#If you wish to save your model, enter the name here
MODEL_SAVE_NAME = "model.pkl"

data_path = os.path.join(curdir, data)
df = pd.read_csv(data_path)
print("Original df shape: ", df.shape)

config_options = ['Vector-Length','Streaming-Vector-Length','Fetch-Block-Size','Loop-Buffer-Size', \
                  'Loop-Detection-Threshold','Heap-Size','Stack-Size','GeneralPurpose-Count', \
                  'FloatingPoint/SVE-Count','Predicate-Count','Conditional-Count','Commit','FrontEnd', \
                  'LSQ-Completion','ROB','Load','Store','Access-Latency','Load-Bandwidth','Store-Bandwidth', \
                  'Permitted-Requests-Per-Cycle','Permitted-Loads-Per-Cycle','Permitted-Stores-Per-Cycle', \
                  'clw','core_clock','l1_latency','l1_clock','l1_associativity','l1_size','l2_latency', \
                  'l2_clock','l2_associativity','l2_size','ram_timing','ram_clock','ram_size']


cycle_options = ['minibude_cycles', 'stream_cycles', 'tealeaf_cycles', 'minisweep_cycles']

def clean_data(df):
    # Drop rows with -1 in cycle values
    dropped_rows = []
    for index, row in df.iterrows():
        for i in cycle_options:
            if row[i] == -1:
                dropped_rows.append(index)
    #for index, row in df.iterrows():
    #        if row["Vector-Length"] != 128:
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


df = clean_data(df)
total_results = []
result_cols = ["perc_acc", "one_perc", "two_perc", "five_perc", "ten_perc", "twentyfive_perc"] + config_options

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

    X_scaled = X
    Y_scaled = Y

    X_train, X_test, Y_train, Y_test = train_test_split(X_scaled, Y_scaled, test_size=0.2, random_state=42)

    end_time = time.time()
    print("Data prep took ", end_time - start_time, "s")

    start_time = time.time()
    model = DecisionTreeRegressor(random_state=42)


    LOAD_SAVE = False
    SAVE_MODEL = False

    if (LOAD_SAVE):
        model = load_model(MODEL_SAVE_NAME)
    else:
        model.fit(X_train, Y_train)
        if (SAVE_MODEL):
            save_model(model)


    mape_scorer = metrics.make_scorer(metrics.mean_absolute_error)
    perm_imp = permutation_importance(model, X_test, Y_test, random_state=42, n_jobs=1, n_repeats=10, scoring=mape_scorer)

    #Get percentage of total impact that each parameter has made as well as the direction of said impact (+ is fewer cycles)
    perc_imp = []
    for i in perm_imp.importances_mean:
        perc_imp.append((i/sum(abs(perm_imp.importances_mean)))*-100)
    print(perc_imp)

    Y_pred = model.predict(X_test).reshape(-1, 1)
    print("Predicted Y")

    Y_test_df = pd.DataFrame(Y_test, columns=df_cycles.columns)
    Y_pred_df = pd.DataFrame(Y_pred, columns=df_cycles.columns)

    get_data_stats(Y_test_df)
    get_data_stats(Y_pred_df)
    end_time = time.time()
    print("Model training took ", end_time - start_time, "s")


    results = []

    total_pred = len(Y_pred)
    perc_results = []

    #Get mean % accuracy
    total_diff = 0
    for i in range(len(Y_pred)):
        total_diff += abs(1 - (Y_pred[i]/Y_test[i]))
    results.append(float(100 - (total_diff / len(Y_pred)) * 100))

    #Get percentage that fall under several percent boundaries
    for limit_perc in [1, 2, 5, 10, 25]:
        counter = 0
        for i in range(len(Y_pred)):
            if abs(((Y_pred[i] / Y_test[i]) - 1) * 100) < limit_perc:
                counter += 1
        results.append((counter/total_pred)*100)
        print(counter, " out of ", total_pred, " predictions were within ", limit_perc, "%. That is ", (counter/total_pred)*100, "%")


    results += perc_imp

    total_results.append(results)

results_df = pd.DataFrame(columns=result_cols)
for i in total_results:
    results_df.loc[len(results_df), :] = i
results_df.to_csv("model_results.csv", index=False)

#Save a sample of some predictions given a config
#save_sample(200)


