import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


class Predictor(object):
    def __init__(self):
        pass

    def predict(self, message):
        return 'Got: ' + message + "\n"
