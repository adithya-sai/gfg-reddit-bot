from pymodm import EmbeddedMongoModel, fields

class Result(EmbeddedMongoModel):

    score = fields.CharField(blank=True)
    scorers = fields.ListField(fields.CharField(), blank=True)
    first_goal = fields.CharField(blank=True)