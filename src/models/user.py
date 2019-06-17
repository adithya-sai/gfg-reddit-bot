class User():

    def __init__(self, username, points, curr_prediction, prev_prediction, prediction_history):
        self.name = username
        self.points = points
        self.curr_prediction = curr_prediction
        self.prev_prediction = prev_prediction
        self.prediction_history = prediction_history

    def __repr__(self):
        return str(self.__dict__)

    