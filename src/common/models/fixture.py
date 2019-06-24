from pynamodb.models import Model
from pynamodb.attributes import (UnicodeAttribute, NumberAttribute)
from botocore.session import Session

from .result import Result
from .league import League
from .status_index import StatusIndex

class Fixture(Model):

    class Meta:
        table_name = 'gfg-fixtures'
        region = Session().get_config_variable('region')

    fixture_id = NumberAttribute(hash_key=True)
    home = UnicodeAttribute()
    away = UnicodeAttribute()
    start_time = NumberAttribute()
    status = UnicodeAttribute()
    status_index = StatusIndex()

    result = Result(null=True)
    league = NumberAttribute()