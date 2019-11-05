import csv
import numpy as np
from sklearn.preprocessing import LabelBinarizer
from sklearn.preprocessing import OneHotEncoder
import tensorflow as tf
from tensorflow.keras import layers
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"]="3"

# Preprocess historical train running data so that it's for training the NN
# Expects ordered data in the form of a CSV file
# The particular types of data are documented in "DataMining.Py"
# Most of the data is one-hot encoded
# Departure Delay is a very strong influence on arrival delay, as such I
# decided not to normalise it and have it act as a "bias".
def preprocess(filename):
    training_data_size = 0
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if(row):
                training_data_size += 1
    
  #These need to be binary encoded
    training_data_LDpairs = [0]*training_data_size
    training_data_times = [0]*training_data_size
    training_data_months = [0]*training_data_size
    training_data_days = [0]*training_data_size
    
    #These don't
    training_data_delays = np.zeros((training_data_size, 1))
    
    #These are the correct delay times to compare the NN prediction to
    actual_outputs = np.zeros((training_data_size, 1))
    
    with open(filename) as csvfile:
        
        reader = csv.reader(csvfile)
        i = 0
        for row in reader:
            if(row):
                trainingData = row[:-1]
                actual_outputs[i] = row[-1]
                training_data_LDpairs[i] = trainingData[0] + "to" + trainingData[1]
                training_data_times[i] = trainingData[2]
                training_data_days[i] = trainingData[3]
                training_data_months[i] = trainingData[4]
                training_data_delays[i] = trainingData[5]
                i += 1
    
    #We need to know which routes the neural net is trained to predict delays
    #for. As such, we save a list of routes we have trained
    trained_routes = set(training_data_LDpairs)
    with open('TrainedRoutes.txt', 'w') as g:
        for route in trained_routes:
            g.write(route+'\n')
    
    lb = LabelBinarizer()
    
    #One hot encode LD pairs
    lb.fit(training_data_LDpairs)
    training_data_LDpairs = lb.transform(training_data_LDpairs)

    #One hot encode months
    lb.fit(training_data_months)
    training_data_months = lb.transform(training_data_months)
    
    #One hot encode days
    lb.fit(training_data_days)
    training_data_days = lb.transform(training_data_days)
    
    #We treat time as a categorical variable where times of day fall in to
    #the category of "morning", "afternoon", "evening", "night"
    #Then we one-hot encode it of course!
    categorical_time = {}
    categorical_time.update(dict.fromkeys(['00', '01', '02', '03', '04', '05'], "night"))
    categorical_time.update(dict.fromkeys(['06', '07', '08', '09', '10', '11'], "morning"))
    categorical_time.update(dict.fromkeys(['12', '13', '14', '15', '16', '17'], "afternoon"))
    categorical_time.update(dict.fromkeys(['18', '19', '20', '21', '22', '23'], "evening"))
    training_data_times = [categorical_time[time[:2]] for time in training_data_times]
    lb.fit(training_data_times)
    training_data_times = lb.transform(training_data_times)
    
    #Output
    training_data = np.concatenate(
            (training_data_LDpairs,
            training_data_times,
            training_data_months,
            training_data_days,
            training_data_delays
            ), axis=1)
    
    
    return np.float32(training_data), np.float32(actual_outputs) #TensorFlow likes float32


# Feel free to add an extra layer by uncommenting the "model.add" line, and
# increasing the number in the first paramater passed to "Dense".     
# I didn't get any increase in accuracy from any combination of increased
# nodes/layers that I tried.
# @valSplit is the percent of data to be used as validation data during training
# @epochs is number of iterations over the training set    
def train(file, epochs=100, valSplit=0.1, batchSize=32):
    
    input_data, output_data = preprocess(file)
    #shuffle the data
    indices = np.arange(input_data.shape[0])
    np.random.shuffle(indices)
    input_data = input_data[indices]
    output_data = output_data[indices]
    shape = input_data[0].shape
    model = tf.keras.Sequential()
    model.add(layers.Dense(32, activation = 'relu', input_shape=shape))
    #model.add(layers.Dropout(0.2))
    #model.add(layers.Dense(128, activation = 'relu'))
    #model.add(layers.Dropout(0.2))
    #model.add(layers.Dense(144, activation = 'relu'))
    #model.add(layers.Dropout(0.2))
    model.add(layers.Dense(1))
    model.compile(optimizer="sgd",
                  loss='mae',
                  metrics=['accuracy', 'mae'])
    model.fit(input_data, output_data, batch_size=batchSize, epochs=epochs, validation_split = valSplit)
    model.save('NN.h5')

# Expects parameters as follows:
# @location : CRS code of current location
# @destination : CRS code of current destination
# @time : STRING time of day in 24 hour format (e.g. 2349)
# @day : day of week as "WEEKDAY", "SATURDAY" or "SUNDAY"
# @month : STRING month as number 1-12
# @delay : INTEGER departure delay
# OUTPUT: A prediction of how long the train's arrival will be delayed     
def predict(location, destination, time, day, month, delay):
    
    LDpairs = []
    with open('TrainedRoutes.txt', 'r') as g:
        for line in g:
            LDpairs.append(line[:-1])
    lb = LabelBinarizer()        
    lb.fit(LDpairs)
    LD = location + "to" + destination
    LD = lb.transform([LD])
    
    #format time
    categorical_time = {}
    categorical_time.update(dict.fromkeys(['00', '01', '02', '03', '04', '05'], "night"))
    categorical_time.update(dict.fromkeys(['06', '07', '08', '09', '10', '11'], "morning"))
    categorical_time.update(dict.fromkeys(['12', '13', '14', '15', '16', '17'], "afternoon"))
    categorical_time.update(dict.fromkeys(['18', '19', '20', '21', '22', '23'], "evening"))
    lb.fit(["night", "morning", "afternoon", "evening"])
    time = lb.transform([categorical_time[time[:2]]])
    
    #format day
    day_categories = ["WEEKDAY", "SATURDAY", "SUNDAY"]
    lb.fit(day_categories)
    day = lb.transform([day])
    
    #format month
    months = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
    lb.fit(months)
    month = lb.transform([month])
    
    args = np.concatenate((LD, time, month, day, [[delay]]), axis=1)
    tf.keras.backend.clear_session()
    model = tf.keras.models.load_model('NN.h5')
    return model.predict(args)[0][0]

if __name__ == "__main__":
    #train("TrainingData.csv", epochs=1000, valSplit=0.2, batchSize=1000)
    print(predict("NRW", "LST", "0800", "WEEKDAY", "1", 0))       
