import Database_controller
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
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
    t_arr_delay = np.zeros((t_size, 1))

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
        t_arr_delay[i] = row[5]

    #Record trained routes
    t_routes = set(t_dep_arr)
    with open("Trained_routes.txt", "w") as tr:
        for r in t_routes:
            tr.write(r+"\n")

    #One hot encode categorical data
    #https://machinelearningmastery.com/how-to-one-hot-encode-sequence-data-in-python/

    # t_time_dep = categorise_time_peak(t_time_arr, t_day)
    t_time_dep = categorise_time_timeofday(t_time_dep)
    t_time_dep = one_hot_encode(t_time_dep)

    # t_time_arr = categorise_time_peak(t_time_arr, t_day)
    t_time_arr = categorise_time_timeofday(t_time_arr)
    t_time_arr = one_hot_encode(t_time_arr)
    

    t_dep_arr  = one_hot_encode(t_dep_arr)
    t_day      = one_hot_encode(t_day)
    t_month    = one_hot_encode(t_month)

    t_data = np.concatenate((t_dep_arr, t_time_dep, t_dep_delay, t_time_arr, t_arr_delay, t_month, t_day),
     axis=1)
    return t_data, t_act_delay

def one_hot_encode(data):
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
##################################################################################################
#                                    Prediction & Evalutation
##################################################################################################
def predict(model_file, datum):
    kNN = load(model_file) 
    print(kNN.predict([datum]))

def evaluate_accuracy(predicted, actual):
    return accuracy_score(predicted, actual)

##################################################################################################
#                                          kNN regression
##################################################################################################
def train_kNN(training, actual, k, file_name):
    #https://skcikit-learn.org/stable/modules/generated/sklearn.neighbors.NearestNeighbors.html#sklearn.neighbors.NearestNeighbors
    training, actual = shuffleData(training, actual)
    kNN = KNeighborsRegressor(n_neighbors=k)
    kNN.fit(training, actual)
    #https://scikit-learn.org/stable/modules/model_persistence.html
    dump(kNN, file_name)

##################################################################################################
#                                          Neural Network 
##################################################################################################
def train_neural_network(training, actual, h_layers, file_name):
    training, actual = shuffleData(training, actual)
    
    nn = MLPRegressor(hidden_layer_sizes=h_layers)
    nn.fit(training, np.ravel(actual))
    dump(nn, file_name)


##################################################################################################
#                                       Testing and Training
##################################################################################################
def main():
    print("Pre-processing.....")
    data, actual = data_preprocessing()

    train_d, test_d, train_a, test_a = split_data(data, actual, 0.4)

    # print("Training kNN.....")
    # train_kNN(data, actual, 3, "3NN_model.joblib")
    # train_kNN(data, actual, 10, "10NN_model.joblib")
    
    print("Training Neural Network......")
    train_neural_network(data, actual, 2, "2_layer_MLP.joblib")


    predict("3NN_model.joblib", data[10])
    predict("2_layer_MLP.joblib", data[10])

if __name__ == '__main__':
    main()