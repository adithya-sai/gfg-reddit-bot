from botocore.session import Session
from pynamodb.attributes import NumberAttribute
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection


class FixtureIndex(GlobalSecondaryIndex):
    """
    This class represents a global secondary index
    """

    class Meta:
        # index_name is optional, but can be provided to override the default name
        index_name = 'fixture_id-index'
        read_capacity_units = 1
        write_capacity_units = 1
        # All attributes are projected
        projection = AllProjection()
        region = Session().get_config_variable('region')
        host = "http://localhost:8000"

    # This attribute is the hash key for the index
    # Note that this attribute must also exist
    # in the model
    fixture_id = NumberAttribute(hash_key=True)
