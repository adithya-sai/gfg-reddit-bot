class Prediction():

    def __init__(self, fixture_id, result):
        self.fixture_id = fixture_id
        self.result = result
    
    def __repr__(self):
        return str(self.__dict__)