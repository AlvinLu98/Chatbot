import Database_controller
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler

from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, VotingRegressor

from sklearn.model_selection import train_test_split, cross_validate, GridSearchCV
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from joblib import dump, load

##################################################################################################
#                                        Data preparation
##################################################################################################
def get_training_data():
    rows = Database_controller.get_all_historical_data()
    return rows


def data_preprocessing():
    rows = get_training_data()
    t_size = len(rows)

    #Categorical variables
    t_dep_arr     = [0]*t_size
    t_day         = [0]*t_size
    t_time_dep    = [0]*t_size
    t_time_arr    = [0]*t_size
    t_month       = [0]*t_size

    #Continuous variables
    t_dep_delay = np.zeros((t_size, 1))

    #Actual delay data
    t_act_delay = np.zeros((t_size, 1))

    #Data structure of historical data:
    # [0] = Origin
    # [1] = Expected departure
    # [2] = Departure delay
    # [3] = Destination
    # [4] = Expected arrival
    # [5] = Arrival delay
    # [6] = Month
    # [7] = Day
    # [8] = TOC
    for i, row in enumerate(rows):
        t_act_delay[i] = row[5]
        t_dep_arr[i]   = row[0] + " to " + row[3]
        t_day[i]       = row[7]
        t_time_dep[i]  = row[1]
        t_time_arr[i]  = row[4]
        t_month[i]     = row[6]
        t_dep_delay[i] = row[2]

    #Record trained routes
    t_routes = set(t_dep_arr)
    with open("Trained_routes.txt", "w") as tr:
        for r in t_routes:
            tr.write(r+"\n")

    #One hot encode categorical data
    #https://machinelearningmastery.com/how-to-one-hot-encode-sequence-data-in-python/

    # t_time_dep = categorise_time_peak(t_time_arr, t_day)
    t_time_dep = categorise_time_timeofday(t_time_dep)
    t_time_dep = one_hot_encode_data(t_time_dep)

    # t_time_arr = categorise_time_peak(t_time_arr, t_day)
    t_time_arr = categorise_time_timeofday(t_time_arr)
    t_time_arr = one_hot_encode_data(t_time_arr)
    

    t_dep_arr  = one_hot_encode_data(t_dep_arr)
    t_day      = one_hot_encode_data(t_day)
    t_month    = one_hot_encode_data(t_month)

    t_data = np.concatenate((t_dep_arr, t_time_dep, t_dep_delay, t_time_arr, t_month, t_day),
     axis=1)
    return t_data, t_act_delay

def one_hot_encode_data(data):
    le = LabelEncoder()
    ohe = OneHotEncoder(sparse=False)

    int_encoded = le.fit_transform(data) 
    int_encoded = int_encoded.reshape(len(int_encoded), 1)
    return ohe.fit_transform(int_encoded)

def categorise_time_timeofday(data):
    #https://thispointer.com/python-6-different-ways-to-create-dictionaries/
    c_time = {}
    c_time.update(dict.fromkeys(['00', '01', '02', '03', '04', '05'], "night"))
    c_time.update(dict.fromkeys(['06', '07', '08', '09', '10', '11'], "morning"))
    c_time.update(dict.fromkeys(['12', '13', '14', '15', '16', '17'], "afternoon"))
    c_time.update(dict.fromkeys(['18', '19', '20', '21', '22', '23'], "evening"))
    
    c_data = [c_time[time[:2] ] for time in data]
    return c_data

def categorise_time_peak(data, day_of_week):
    c_peak = {'WEEKDAY':{}, 'SATURDAY':{}, 'SUNDAY':{}}
    c_peak['WEEKDAY'].update(dict.fromkeys(['00', '01', '02', '03', '04', '05', '06', '07', '08', '09'], "Off-peak"))
    c_peak['WEEKDAY'].update(dict.fromkeys(['10', '11'], "Super Off-peak"))
    c_peak['WEEKDAY'].update(dict.fromkeys(['12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23'], "Peak"))

    c_peak['SATURDAY'].update(dict.fromkeys(['00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
    '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23'], "Off-peak"))

    c_peak['SUNDAY'].update(dict.fromkeys(['00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
    '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23'], "Off-peak"))

    c_data = [0]*len(data)
    for i, time in enumerate(data):
        if day_of_week[i] == "WEEKDAY":
            c_data[i] = c_peak['WEEKDAY'][time[:2]]
            print(c_data[i])
        elif day_of_week[i] == "SATURDAY":
            c_data[i] = c_peak['SATURDAY'][time[:2]]
        else:
            c_data[i] = c_peak['SUNDAY'][time[:2]]

def shuffleData(data, actual):
    #https://tech.pic-collage.com/tips-of-numpy-shuffle-multiple-arrays-e4fb3e7ae2a
    permutation = np.random.permutation(data.shape[0])
    data = data[permutation]
    actual = actual[permutation]
    return data, actual

def split_data(data, actual, t_size):
    train_d, test_d, train_a, test_a = train_test_split(data, actual, test_size=t_size, random_state=4)
    return train_d, test_d, train_a, test_a

def format_data(dep, arr, dep_time, dep_delay, arr_time, month, day):
    dep_arr = dep + " to  " + arr
    dep_arr_list = []
    with open("Train_routes.txt", 'r') as tr:
        for rows in tr:
            dep_arr_list.append(rows)
    print(dep_arr_list)
    
    one_hot_encode_value(dep_arr_list, dep_arr)
    
    months = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
    month = one_hot_encode_value(months, month)

    day_type = ["WEEKDAY", "SATURDAY", "SUNDAY"]
    day = one_hot_encode_value(day_type, day)

    time_of_day = ["night", "morning", "afternoon", "evening"]
    dep_time = categorise_time_timeofday([dep_time])
    arr_time = categorise_time_timeofday([arr_time])
    dep_time = one_hot_encode_value(time_of_day, dep_time)
    arr_time = one_hot_encode_value(time_of_day, arr_time)

    input_data = np.concatenate((dep_arr, dep_time, dep_delay, arr_time, month, day), axis=1)
    return input_data

def one_hot_encode_value(fit, value):
    le = LabelEncoder()
    ohe = OneHotEncoder(sparse=False)

    le.fit(fit)
    int_encoded = le.transform([value])
    int_encoded = int_encoded.reshape(len(int_encoded), 1)
    print(int_encoded)
    one_hot_encoded = ohe.fit_transform(int_encoded)
    return one_hot_encoded

##################################################################################################
#                                    Prediction & Evalutation
##################################################################################################
def predict(model_file, datum):
    model = load(model_file) 
    return model.predict(datum)

def predict_values(model_file, dep, arr, dep_time, dep_delay, arr_time, month, day):
    input_data = format_data(dep, arr, dep_time, dep_delay, arr_time, month, day)
    return predict(model_file, input_data)


def evaluate_mean_abs_err(actual, predicted):
    return mean_absolute_error(actual, predicted)

def evaluate_mean_sqr_err(actual, predicted):
    return mean_squared_error(actual, predicted)

def evaluate_r2_score(actual, predicted):
    return r2_score(actual, predicted)

##################################################################################################
#                                        Cross Validation
##################################################################################################
def cross_validate_model(model, train, target, fold):
    return cross_validate(model, train, target, 
    scoring=('explained_variance','r2', 'neg_mean_absolute_error', 'neg_mean_squared_error'), cv=fold)

##################################################################################################
#                                          kNN regression
##################################################################################################
def train_kNN(training, actual, k, file_name):
    #https://skcikit-learn.org/stable/modules/generated/sklearn.neighbors.NearestNeighbors.html#sklearn.neighbors.NearestNeighbors
    kNN = KNeighborsRegressor(n_neighbors=k)
    kNN.fit(training, actual)
    #https://scikit-learn.org/stable/modules/model_persistence.html
    dump(kNN, file_name)
    return kNN

def train_weighted_kNN(training, actual, k, file_name):
    kNN = KNeighborsRegressor(n_neighbors=k, weights='distance')
    kNN.fit(training, actual)
    dump(kNN, file_name)
    return kNN

##################################################################################################
#                                          Neural Network 
##################################################################################################
def train_neural_network(training, actual, h_layers, state, file_name):
    nn = MLPRegressor(hidden_layer_sizes=h_layers, random_state=state, max_iter=2000, early_stopping=True)
    nn.fit(training, np.ravel(actual))
    dump(nn, file_name)
    return nn

##################################################################################################
#                                     Decision tree regression
##################################################################################################
def train_decision_tree(training, actual, depth, file_name):
    dt = DecisionTreeRegressor(max_depth=depth, random_state=1)
    dt.fit(training, actual)
    dump(dt, file_name)
    return dt

##################################################################################################
#                                     Random forest regression
##################################################################################################
def train_random_forest(training, actual, n_trees, depth, file_name):
    rf = RandomForestRegressor(n_estimators=n_trees, max_depth=depth, random_state=1) 
    rf.fit(training, np.ravel(actual))
    dump(rf, file_name)
    return rf

##################################################################################################
#                                        Voting regressor
##################################################################################################
def train_voting_regressor(training, actual, estimators, file_name):
    vr = VotingRegressor(estimators)
    vr.fit(training, actual)
    dump(vr, file_name)
    return vr

##################################################################################################
#                                       Testing and Training
##################################################################################################
def main():
    print("-------------------------------- Pre-processing --------------------------------")
    data, actual = data_preprocessing()

    train_d, test_d, train_a, test_a = split_data(data, actual, 0.4)

    train_d, train_a = shuffleData(train_d, train_a)
    data, actual = shuffleData(data, actual)

    print("----------------------------------- Training -----------------------------------")
    print("Neural Network.....")
    train_neural_network(train_d, train_a, (5, 10), 4, "2_layer_NN.joblib")
    # mlp = MLPRegressor(early_stopping=True, max_iter=2000)
    # parameter_space = {
    #     'hidden_layer_sizes': [(2,), (3,), (4,), (5,), (10,), (15,), (20,)],
    #     'random_state': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # }
    # best_val = GridSearchCV(mlp, parameter_space, n_jobs=-1, cv=3)
    # best_val.fit(data, np.ravel(actual))
    # print("Best params: ", best_val.best_params_)
    # dump(best_val.best_estimator_, "BEST_NN.joblib")

    # print("Decision Tree.....")
    # train_decision_tree(train_d, train_a, None, "decision_tree_nomax.joblib")

    # print("Random forest.....")
    # train_random_forest(train_d, train_a, 4, None, "random_forest.joblib")

    print("---------------------------------- Prediction ----------------------------------")   
    nn_pred = predict("2_layer_NN.joblib", test_d)
    # dt_pred = predict("decision_tree_nomax.joblib", test_d)
    # rf_pred = predict("random_forest.joblib", test_d)

    best_nn_pred = predict("BEST_NN.joblib", test_d)
    print(evaluate_r2_score(test_a, best_nn_pred))

    print(evaluate_r2_score(test_a, nn_pred))
    # print(evaluate_r2_score(test_a, dt_pred))
    # print(evaluate_r2_score(test_a, rf_pred))

    print("----------------------------------- Testing ------------------------------------")
    # print("Neural network.....")
    # nn = MLPRegressor(hidden_layer_sizes=(2,), solver='sgd', random_state=3, max_iter=1000)
    # result = cross_validate_model(nn, data, np.ravel(actual), 3)
    # print(result['test_r2'])

    # print("Decision tree.....")
    # dt = DecisionTreeRegressor()
    # result = cross_validate_model(dt, data, actual, 3)
    # print(result['test_r2'])

    # print("Random forest.....")
    # rf = RandomForestRegressor(n_estimators=4)
    # result = cross_validate_model(rf, data, actual, 3)
    # print(result['test_r2'])

    # print("3NN.....")
    # kNN_3 = KNeighborsRegressor(n_neighbors=3)
    # result = cross_validate_model(kNN_3, data, actual, 3)
    # print(result['test_r2'])

    # print("10NN.....")
    # kNN = KNeighborsRegressor(n_neighbors=10)
    # result = cross_validate_model(kNN, data, actual, 3)
    # print(result['test_r2'])

if __name__ == '__main__':
    main()