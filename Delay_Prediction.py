import Database_controller

def get_training_data():
    rows = Database_controller.get_all_historical_data()
    return rows

def data_preprocessing():
    rows = get_training_data()
    training_size = len(rows)