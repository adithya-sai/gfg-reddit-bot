from pymodm import MongoModel, fields
from models.result import Result
from models.league import League

class Fixture(MongoModel):

    fixture_id = fields.BigIntegerField(primary_key=True)
    home = fields.CharField()
    away = fields.CharField()
    start_time = fields.BigIntegerField()
    status = fields.CharField()
    result = fields.EmbeddedDocumentField(Result, blank=True)
    league = fields.ReferenceField(League)