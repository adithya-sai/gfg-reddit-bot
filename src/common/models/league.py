from botocore.session import Session
from pynamodb.attributes import (UnicodeAttribute, NumberAttribute)
from pynamodb.models import Model


class League(Model):
    class Meta:
        table_name = "gfg-leagues"
        region = Session().get_config_variable('region')
        host = "http://localhost:8000"

    league_id = NumberAttribute(hash_key=True)
    league_name = UnicodeAttribute()
