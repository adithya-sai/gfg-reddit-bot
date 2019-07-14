from pynamodb.models import Model
from pynamodb.attributes import (UnicodeAttribute, MapAttribute)
from botocore.session import Session

class Stat(Model):

    class Meta:
        table_name = "gfg-stats"
        region = Session().get_config_variable('region')

    stat_name = UnicodeAttribute(hash_key=True)
    stat_value = MapAttribute()
