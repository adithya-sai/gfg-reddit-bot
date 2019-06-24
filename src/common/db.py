from common.models.fixture import Fixture
from common.models.submission import Submission
from common.models.user import User


def get_fixtures_by_status(status):
    return list(Fixture.objects.raw({'status': status}).aggregate({'$sort': {'start_time': 1}}, {'$limit' : 1 }))

def get_fixture_by_id(fixture_id):
    try:
        return Fixture.objects.get({'_id': fixture_id})
    except Fixture.DoesNotExist:
        return None

def save_submission(id, fixture_id, created_at):
    Submission(id, fixture_id, created_at).save()

def change_fixture_status(fixture, status):
    fixture.status = status
    fixture.save()

def get_submission_by_fixture(fixture_id):
    try:
        return Submission.objects.get({'fixture_id': fixture_id})
    except Submission.DoesNotExist:
        return None

def get_user_by_id(user_id):
        
    user_list = list(User.objects.raw({'_id': user_id}))
    if len(user_list) > 0:
        return user_list[0]
    else:
        return None

def insert_users_in_bulk(users):
    User.objects.bulk_create(users)




