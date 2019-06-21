from pymongo import MongoClient
from pymodm.connection import connect
from models.fixture import Fixture
from models.submission import Submission

connect("mongodb://localhost:27017/gfg_db")

def get_new_fixtures():
    return list(Fixture.objects.raw({'status': "NS"}).aggregate({'$sort': {'start_time': 1}}, {'$limit' : 1 }))

def get_fixture_by_id(fixture_id):
    f = Fixture.objects.get({'_id': fixture_id})
    return f

def save_submission(id, fixture_id, created_at):
    Submission(id, fixture_id, created_at).save()

def change_fixture_status(fixture, status):
    fixture.status = status
    fixture.save()



