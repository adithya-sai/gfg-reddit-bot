from pymodm import EmbeddedMongoModel, fields

class Result(EmbeddedMongoModel):
    home_goals = fields.IntegerField()
    away_goals = fields.IntegerField()
    scorers = fields.ListField(fields.CharField(), blank=True)
    first_event = fields.CharField(blank=True)