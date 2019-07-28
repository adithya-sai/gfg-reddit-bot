from botocore.session import Session
from pynamodb.attributes import UnicodeAttribute, NumberAttribute
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection


class StatusIndex(GlobalSecondaryIndex):
    """
    This class represents a global secondary index
    """

    class Meta:
        # index_name is optional, but can be provided to override the default name
        index_name = 'status-start_time-index'
        read_capacity_units = 2
        write_capacity_units = 1
        # All attributes are projected
        projection = AllProjection()
        region = Session().get_config_variable('region')
        host = "http://localhost:8000"

    # This attribute is the hash key for the index
    # Note that this attribute must also exist
    # in the model
    status = UnicodeAttribute(hash_key=True)
    start_time = NumberAttribute(range_key=True)
