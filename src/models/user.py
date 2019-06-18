from pymodm import MongoModel, EmbeddedMongoModel, fields
from models.league import League
from models.result import Result
from models.fixture import Fixture

class PointPerLeague(EmbeddedMongoModel):
    league_id = fields.ReferenceField(League)
    points = fields.IntegerField()

class Points(EmbeddedMongoModel):
        total = fields.IntegerField()
        points_per = fields.EmbeddedDocumentField(PointPerLeague) 

class Prediction(EmbeddedMongoModel):

    fixture = fields.ReferenceField(Fixture)
    result = fields.EmbeddedDocumentField(Result)

class User(MongoModel):

    username = fields.CharField(primary_key=True)
    points = fields.EmbeddedDocumentField(Points, blank=True)
    curr_prediction = fields.EmbeddedDocumentField(Prediction, blank=True)
    prediction_history = fields.EmbeddedDocumentListField(Prediction, blank=True)

