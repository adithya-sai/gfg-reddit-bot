class Result():
    def __init__(self, score, scorers, goal_times):
        self.score = score
        self.scorers = scorers
        self.goal_times = goal_times

    def __repr__(self):
        return str(self.__dict__)