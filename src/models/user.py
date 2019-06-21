from pymodm import MongoModel, EmbeddedMongoModel, fields
from models.league import League
from models.result import Result
from models.fixture import Fixture

class Points(EmbeddedMongoModel):
        total = fields.IntegerField()
        points_per = fields.DictField() 

class Prediction(EmbeddedMongoModel):

    fixture = fields.ReferenceField(Fixture)
    result = fields.EmbeddedDocumentField(Result)
    posted_at = fields.BigIntegerField()
    points = fields.IntegerField()

class User(MongoModel):

    username = fields.CharField(primary_key=True)
    points = fields.EmbeddedDocumentField(Points, blank=True)
    curr_prediction = fields.EmbeddedDocumentField(Prediction)
    prediction_history = fields.EmbeddedDocumentListField(Prediction, blank=True)

