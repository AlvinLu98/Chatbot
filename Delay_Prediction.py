import Database_controller
import numpy as np
from sklearn.preprocessing import LabelEncoder, LabelBinarizer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler

from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, VotingRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.svm import LinearSVR

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
    dep_arr = dep + " to " + arr + "\n"
    dep_arr_list = []
    with open("Trained_routes.txt", 'r') as tr:
        for rows in tr:
            dep_arr_list.append(rows)
    
    dep_arr = one_hot_encode_value(dep_arr_list, dep_arr)
    
    months = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
    month = one_hot_encode_value(months, month)

    day_type = ["WEEKDAY", "SATURDAY", "SUNDAY"]
    day = one_hot_encode_value(day_type, day)

    time_of_day = ["night", "morning", "afternoon", "evening"]
    dep_time = categorise_time_timeofday([dep_time])
    arr_time = categorise_time_timeofday([arr_time])
    dep_time = one_hot_encode_value(time_of_day, dep_time[0])
    arr_time = one_hot_encode_value(time_of_day, arr_time[0])
    input_data = np.concatenate((dep_arr, dep_time, [[int(dep_delay)]], arr_time, month, day), axis=1)
    return input_data

def one_hot_encode_value(fit, value):
    lb = LabelBinarizer()
    lb.fit(fit)
    one_hot_encoded = lb.transform([value])
    return one_hot_encoded

##################################################################################################
#                                    Prediction & Evalutation
##################################################################################################
def predict_sets(model_file, datum):
    model = load(model_file) 
    return model.predict(datum)

def predict(model_file, datum):
    model = load(model_file) 
    # print(model.get_params)
    return model.predict([datum])

def predict_values(model_file, dep, arr, dep_time, dep_delay, arr_time, month, day):
    input_data = format_data(dep, arr, dep_time, dep_delay, arr_time, month, day)
    model = load(model_file) 
    return model.predict(input_data)


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
#                                       Linear regression
##################################################################################################
def train_ridge_reg(training, actual, file_name):
    rid_reg = Ridge(random_state=2)
    rid_reg.fit(training, np.ravel(actual))
    dump(rid_reg, file_name)
    return rid_reg

##################################################################################################
#                                       Support vector machine
##################################################################################################
def train_SVC(training, actual, file_name):
    svc = LinearSVR()
    svc.fit(training, np.ravel(actual))
    dump(svc, file_name)
    return svc

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
#                                        Gradient boosting
##################################################################################################
def train_gradient_boosting(training, actual, file_name):
    gb = GradientBoostingRegressor()
    gb.fit(training, np.ravel(actual))
    dump(gb, file_name)
    return gb

##################################################################################################
#                                        Voting regressor
##################################################################################################
def train_voting_regressor(training, actual, estimators, file_name):
    vr = VotingRegressor(estimators)
    vr.fit(training, np.ravel(actual))
    dump(vr, file_name)
    return vr

##################################################################################################
#                                       Testing and Training
##################################################################################################
def main():
    print("-------------------------------- Pre-processing --------------------------------")
    data, actual = data_preprocessing()

    train_d, test_d, train_a, test_a = split_data(data, actual, 0.4)

    # train_d, train_a = shuffleData(train_d, train_a)
    # data, actual = shuffleData(data, actual)

    print("----------------------------------- Training -----------------------------------")
    print("Ridge Regressor.....")
    # train_ridge_reg(train_d, train_a, "Linear_Regressor.joblib")
    # ridge_reg = Ridge()
    # parameter_space = {
    #     'alpha': [1.0, 2.0, 3.0, 5.0, 10.0],
    #     'random_state': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # }
    # best_val = GridSearchCV(ridge_reg, parameter_space, n_jobs=-1, cv=3)
    # best_val.fit(data, np.ravel(actual))
    # print("Best params: ", best_val.best_params_)
    # dump(best_val.best_estimator_, "BEST_Ridge.joblib")
    
    print("Support Vector Machine.....")
    # train_SVC(train_d, train_a, "SVC.joblib")
    # ridge_reg = Ridge()
    # parameter_space = {
    #     'C': [1.0, 1.5, 2.0, 3.0, 5.0, 10.0],
    #     'random_state': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # }
    # best_val = GridSearchCV(ridge_reg, parameter_space, n_jobs=-1, cv=3)
    # best_val.fit(data, np.ravel(actual))
    # print("Best params: ", best_val.best_params_)
    # dump(best_val.best_estimator_, "BEST_Ridge.joblib")

    print("Neural Network.....")
    # train_neural_network(train_d, train_a, (5, 32), 4, "2_layer_NN.joblib")
    # mlp = MLPRegressor(early_stopping=True, max_iter=2000)
    # parameter_space = {
    #     'hidden_layer_sizes': [(3,32), (20,32), (20,64), (4,64), (3,64), (3,128), (2,128), (2,64)]
    # }
    # best_val = GridSearchCV(mlp, parameter_space, n_jobs=-1, cv=3)
    # best_val.fit(data, np.ravel(actual))
    # print("Best params: ", best_val.best_params_)
    # dump(best_val.best_estimator_, "BEST_NN_2.joblib")

    print("Decision Tree.....")
    train_decision_tree(train_d, train_a, None, "decision_tree_nomax.joblib")
    dt =  DecisionTreeRegressor()
    parameter_space = {
        'criterion': ["mse", "mae", "friedman_mse"],
        'max_depth': [None, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25],
        'random_state': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    }
    best_tree = GridSearchCV(dt, parameter_space, n_jobs=-1, cv=3)
    best_tree.fit(data, np.ravel(actual))
    print("Best params: ", best_tree.best_params_)
    dump(best_tree.best_estimator_, "BEST_Tree_2.joblib")

    print("Random forest.....")
    # train_random_forest(train_d, train_a, 4, None, "random_forest.joblib")

    # rf =  RandomForestRegressor()
    # parameter_space = {
    #     'n_estimators': [2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25],
    #     'max_depth': [2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25],
    #     'random_state': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # }
    # best_forest = GridSearchCV(rf, parameter_space, n_jobs=-1, cv=3)
    # best_forest.fit(data, np.ravel(actual))
    # print("Best params: ", best_forest.best_params_)
    # dump(best_tree.best_estimator_, "BEST_Forest.joblib")

    print("Gradient boosting.....")
    # train_gradient_boosting(train_d, train_a, "Gradient_Boosting.joblib")

    print("Voting regressor.....")
    # nn = MLPRegressor(early_stopping=True, hidden_layer_sizes=(20,32), max_iter=2000)
    # nn2 = MLPRegressor(early_stopping=True, hidden_layer_sizes=(2,64), max_iter=2000)
    # tree = DecisionTreeRegressor(max_depth=8, random_state=4)

    # train_voting_regressor(train_d, train_a, [("Neural_1",nn), ("Neural_2",nn2) ,("Tree",tree)], "Voting_Regressor.joblib")

    print("---------------------------------- Prediction ----------------------------------")   
    lin_pred = predict_sets("Linear_Regressor.joblib", test_d)
    print("Linear regression:      ", evaluate_r2_score(test_a, lin_pred), evaluate_mean_abs_err(test_a, lin_pred))
    
    svc_pred = predict_sets("SVC.joblib", test_d)
    print("Support vactor machine: ", evaluate_r2_score(test_a, svc_pred), evaluate_mean_abs_err(test_a, svc_pred))

    nn_pred = predict_sets("2_layer_NN.joblib", test_d)
    print("Neural network:         ", evaluate_r2_score(test_a, nn_pred), evaluate_mean_abs_err(test_a, nn_pred))

    dt_pred = predict_sets("decision_tree_nomax.joblib", test_d)
    print("Decision tree:          ", evaluate_r2_score(test_a, dt_pred), evaluate_mean_abs_err(test_a, dt_pred))

    gb_pred = predict_sets("Gradient_Boosting.joblib", test_d)
    print("Gradient boosting:      ", evaluate_r2_score(test_a, gb_pred), evaluate_mean_abs_err(test_a, gb_pred))

    rf_pred = predict_sets("random_forest.joblib", test_d)
    print("Random forest:          ", evaluate_r2_score(test_a, rf_pred), evaluate_mean_abs_err(test_a, rf_pred))

    best_nn_pred = predict_sets("BEST_NN.joblib", test_d)
    print("Best neural network 1:  ", evaluate_r2_score(test_a, best_nn_pred), evaluate_mean_abs_err(test_a, best_nn_pred))

    best_nn_pred_2 = predict_sets("BEST_NN_2.joblib", test_d)
    print("Best neural network 2:    ", evaluate_r2_score(test_a, best_nn_pred_2), evaluate_mean_abs_err(test_a, best_nn_pred_2))

    best_tree_pred = predict_sets("BEST_Tree.joblib", test_d)
    print("Best decision tree 1:     ", evaluate_r2_score(test_a, best_tree_pred), evaluate_mean_abs_err(test_a, best_tree_pred))

    best_tree_pred_2 = predict_sets("BEST_Tree_2.joblib", test_d)
    print("Best decision tree 1:     ", evaluate_r2_score(test_a, best_tree_pred_2), evaluate_mean_abs_err(test_a, best_tree_pred_2))

    voting_pred = predict_sets("Voting_Regressor.joblib", test_d)
    print("Voting regression:        ", evaluate_r2_score(test_a, best_voting_pred), evaluate_mean_abs_err(test_a, voting_pred))

    best_forest_pred = predict("BEST_Forest.joblib", test_d)
    print("Best random forest:       ", evaluate_r2_score(test_a, best_tree_pred), evaluate_mean_abs_err(test_a, best_forest_pred))

    print("----------------------------------- Values ------------------------------------")
    best_nn = load("BEST_NN.joblib")
    best_nn_2 = load("BEST_NN_2.joblib")
    best_tree = load("BEST_Tree.joblib")
    best_tree_2 = load("BEST_Tree.joblib")

    print("Neural Network 1: ", best_nn.get_params())
    print()

    print("Neural Network 2: ", best_nn_2.get_params())
    print()

    print("Decision Tree 1: ", best_tree.get_params())
    print()

    print("Decision Tree 2: ", best_tree_2.get_params())

if __name__ == '__main__':
    main()