from pynamodb.models import Model
from pynamodb.attributes import (UnicodeAttribute, NumberAttribute, MapAttribute, ListAttribute)
from botocore.session import Session

from .league import League
from .result import Result
from .fixture import Fixture
from .user_points_index import UserPointsIndex

class Prediction(MapAttribute):

    fixture = NumberAttribute()
    result = Result()
    posted_at = NumberAttribute()
    points = NumberAttribute()

class User(Model):

    class Meta:
        table_name = 'gfg-users'
        region = Session().get_config_variable('region')
    user_id = UnicodeAttribute(hash_key=True)
    total_points = NumberAttribute(default_for_new=0)
    points_per_league = MapAttribute()
    curr_prediction = Prediction()
    prediction_history = ListAttribute()
