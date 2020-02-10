from pynamodb.attributes import (MapAttribute, NumberAttribute, ListAttribute)


class Result(MapAttribute):
    home_goals = NumberAttribute()
    away_goals = NumberAttribute()
    home_team_id = NumberAttribute()
    away_team_id = NumberAttribute()
    scorers = ListAttribute(null=True)
    first_event = NumberAttribute()
