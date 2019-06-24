from pynamodb.models import Model
from pynamodb.attributes import (UnicodeAttribute, NumberAttribute)
from botocore.session import Session

class League(Model):

    class Meta:
        table_name = "gfg-leagues"
        region = Session().get_config_variable('region')

    league_id = NumberAttribute(hash_key=True)
    league_name = UnicodeAttribute()
