class Fixture():

    def __init__(self, fixture_id, home, away, start_time, result, type):
        self.fixture_id = fixture_id
        self.home = home
        self.away = away
        self.start_time = start_time
        self.result = result
        self.type = type
        
    def __repr__(self):
        return str(self.__dict__)