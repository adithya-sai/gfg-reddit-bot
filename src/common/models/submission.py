from botocore.session import Session
from pynamodb.attributes import (UnicodeAttribute, NumberAttribute)
from pynamodb.models import Model

from .fixture_index import FixtureIndex


class Submission(Model):
    class Meta:
        table_name = 'gfg-submissions'
        region = Session().get_config_variable('region')
    submission_id = UnicodeAttribute(hash_key=True)
    fixture_id = NumberAttribute()
    fixture_index = FixtureIndex()
    created_at = NumberAttribute()
