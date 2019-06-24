from pynamodb.attributes import (MapAttribute, UnicodeAttribute, NumberAttribute, ListAttribute)

class Result(MapAttribute):
    home_goals = NumberAttribute()
    away_goals = NumberAttribute()
    scorers = ListAttribute()
    first_event = NumberAttribute()