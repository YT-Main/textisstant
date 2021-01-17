import numpy as np

class Government:
    def __init__(self):
        alerts = {"WARNING: The Waterloo Region has issued a lockdown effective effective immediately!": 20,
                "CAUTION: Disastrous weather conditions heading towards Waterloo.  Take precautionary action now!": 20,
                "Citizens, please be advised that Vonage is a cool company.  That's all.  Cheers.": 20,
                "NULL": 60}

        self.keys, weights = zip(*alerts.items())
        self.probabilities = np.array(weights, dtype=float) / float(sum(weights))

    def get_alert(self):
        return np.random.choice(self.keys, 1, p=self.probabilities)[0]

# Created By: Yash Trivedi