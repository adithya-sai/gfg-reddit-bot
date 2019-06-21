from pymodm import MongoModel, fields
from models.fixture import Fixture

class Submission(MongoModel):
    submission_id = fields.CharField(primary_key=True)
    fixture_id = fields.ReferenceField(Fixture)
    created_at = fields.BigIntegerField()