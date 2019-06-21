from pymodm import MongoModel, fields

class League(MongoModel):

    league_id = fields.CharField(primary_key=True)
    league_name = fields.CharField()