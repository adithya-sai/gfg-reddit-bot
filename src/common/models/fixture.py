from botocore.session import Session
from pynamodb.attributes import (UnicodeAttribute, NumberAttribute)
from pynamodb.models import Model

from .result import Result
from .status_index import StatusIndex


class Fixture(Model):
    class Meta:
        table_name = 'gfg-fixtures'
        region = Session().get_config_variable('region')
        host = "http://localhost:8000"

    fixture_id = NumberAttribute(hash_key=True)
    home = UnicodeAttribute()
    away = UnicodeAttribute()
    home_team_id = NumberAttribute()
    away_team_id = NumberAttribute()
    start_time = NumberAttribute()
    status = UnicodeAttribute()
    status_index = StatusIndex()

    result = Result(null=True)
    league = NumberAttribute()
