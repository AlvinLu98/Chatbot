"""
prediction.py

Prediction Model component
"""

import numpy as np
from datetime import datetime, date, time, timedelta
import requests, json, csv

def z_standardise(x, mean, sd):
    """ Computes a standard score.

    Args:
        x: raw score.
        mean: sample mean.
        sd: sample standard deviation.

    Returns:
        Standard z-score of the input.
    """
    return (x - mean) / sd


class KNNRegresser:
    """ Represents a k-NN regression prediction model.

    Attributes:
        n: Dimensionality, i.e. number of features.
        k: Number of nearest-neighbours to sample from.
    """

    def __init__(self, n, k):
        self.n = n
        self.k = k

    def train(self, data):
        """ Trains this model with the given data.

        Args:
            data: List of feature lists, all of length n+1 with the final
                element as the regression variable.
        """
        self._data = np.array(data, dtype=np.float64)

        # Compute mean and corrected standard deviation for each feature
        self._means = np.mean(self._data, axis=0)[:-1]
        self._sds = np.std(self._data, axis=0, ddof=1)[:-1]

        # Z-standardise features
        for i in range(len(self._data)):
            self._data[i][:-1] = np.array(list(map(
                z_standardise, self._data[i][:-1], self._means, self._sds)))

    def predict(self, input):
        """ Predicts the regression variable for the given input.

        Args:
            input: Feature list, of length n.

        Returns:
            Predicted value for regression variable.
        """
        if (len(input) != self.n):
            raise Exception(f"Input list must be of dimensionality {self.n}.")

        # Z-standardise input
        input = list(map(z_standardise, input, self._means, self._sds))

        # Construct array of squared distances (square rooting is unnecessary)
        distances = np.empty(len(self._data))
        for i in range(len(self._data)):
            datum = self._data[i][:-1]
            distances[i] = sum(map(lambda x,y: (x-y)**2, input, datum))

        # Obtain indices of the k smallest distances
        smallest = np.argpartition(distances, self.k)[:self.k]

        # Convert indices to regression variable
        results = [self._data[x][-1] for x in smallest]

        # Calculate regression prediction as mean
        return sum(results) / self.k


def str_to_time(str):
    """ Converts a HSP format time string into a Python time object.

    Args:
        str: Time string in format "HHMM".

    Returns:
        Python time object.
    """
    t = time(int(str[:2]), int(str[2:]))
    return datetime.combine(date.min, t)


def time_to_str(time):
    """ Converts a Python time object into HSP format time string.

    Args:
        time: Python time object.

    Returns:
        Time string in format "HHMM"
    """
    return time.strftime("%H%M")


def predict_arrival_delay(from_loc, to_loc, current_loc, delay):
    """ Trains a regression model from historical data using the given
    parameters to predict an overall delay time.

    Args:
        from_loc: String of starting station code.
        to_loc: String of destination stattion code.
        current_loc: String of current station code.
        delay: Current time delay in minutes.

    Returns:
        Predicted overall time delay in minutes.
    """
    # Configurations for API requests
    metrics_url = "https://hsp-prod.rockshore.net/api/v1/serviceMetrics"
    details_url = "https://hsp-prod.rockshore.net/api/v1/serviceDetails"
    headers = { "Content-Type": "application/json" }
    auths = ("Sam.Griffiths@uea.ac.uk", "AIChatbot3!")

    # Search between current day and 2 days prior
    to_date = datetime.today()
    from_date = to_date - timedelta(days=2)

    # Determine days option from from_date (Mon-Sun is 0-6)
    day_num = from_date.weekday()
    if day_num == 6:
        days = "SUNDAY"
    elif day_num == 5:
        days = "SATURDAY"
    else:
        days = "WEEKDAY"

    data = {
        "from_loc": from_loc,
        "to_loc": to_loc,
        "from_time": "0000",
        "to_time": "2359",
        "from_date": from_date.strftime("%Y-%m-%d"),
        "to_date": to_date.strftime("%Y-%m-%d"),
        "days": days
    }

    # Get RIDs of trains matching the parameters
    r_metrics = requests.post(
        metrics_url, headers=headers, auth=auths, json=data)
    metrics = json.loads(r_metrics.text)
    rids = []
    for s in metrics["Services"]:
        rids.extend(s["serviceAttributesMetrics"]["rids"])
    
    # Training data with elements [current_delay, resultant_delay]
    training_data = []

    # Get service details for each RID
    for rid in rids:
        rid_data = { "rid": rid }
        r_details = requests.post(
            details_url, headers=headers, auth=auths, json=rid_data)
        details = json.loads(r_details.text)

        try:
            # Get current location delay (time from public to actual departure)
            current = next((
                x for x in details["serviceAttributesDetails"]["locations"]
                if x["location"] == current_loc))
            current_delay = (str_to_time(current["actual_td"])
                - str_to_time(current["gbtt_ptd"]))

            # Get destination delay
            destination = details["serviceAttributesDetails"]["locations"][-1]
            resultant_delay = (str_to_time(destination["actual_ta"])
                - str_to_time(destination["gbtt_pta"]))

            # Log delay data in minutes
            training_data.append([current_delay.total_seconds() // 60,
                resultant_delay.total_seconds() // 60])
        # Ignore if current location is missing or lacks required data
        except (StopIteration, ValueError):
            pass

    # Train regression model and obtain prediction
    if not training_data:
        return 0.0

    knnr = KNNRegresser(1, 5)
    knnr.train(training_data)
    return knnr.predict([delay])


def load_csv_dict(filename):
    """ Loads the given two-column CSV file as a dict.

    Args:
        filename: File name string to load.

    Returns:
        dict of CSV contents.
    """
    with open(filename) as csv_file:
        next(csv_file)
        csv_reader = csv.reader(csv_file)
        return dict(csv_reader)


def station_code(name):
    """ Looks up official station codes.

    Args:
        name: String of station name.

    Returns:
        String of station code.
    """
    return station_code.codes[name]
station_code.codes = load_csv_dict("data/station_codes.csv")

def predict(start, destination, current, delay):
    return predict_arrival_delay(station_code(start), station_code(destination), station_code(current), delay)

if __name__ == "__main__":
    #predict_arrival_delay("NRW", "LST", "MNG", 4.0)
    print(predict_arrival_delay(
        station_code("Norwich"),
        station_code("London Liverpool Street"),
        station_code("Manningtree"),
        4.0))
