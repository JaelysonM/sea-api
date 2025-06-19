from datetime import time
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class StoreScheduleEntity:
    store_id: int
    day_of_week: int
    opens_at: Optional[time]
    closes_at: Optional[time]
    is_closed: bool

    class Meta:
        verbose = "Horário da Loja"
        display_name = "StoreSchedule"
        name = "store_schedule"
        filters = ["store_id", "day_of_week", "is_closed"]
        joins = []

    def to_dict(self):
        return asdict(self)


def store_schedule_model_factory(
    store_id: int,
    day_of_week: int,
    opens_at: Optional[time] = None,
    closes_at: Optional[time] = None,
    is_closed: bool = False,
) -> StoreScheduleEntity:
    return StoreScheduleEntity(
        store_id=store_id,
        day_of_week=day_of_week,
        opens_at=opens_at,
        closes_at=closes_at,
        is_closed=is_closed,
    )
