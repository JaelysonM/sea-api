from enum import Enum


class Role(Enum):
    SUPERUSER = {"id": 0, "priority": 0}
    ADMIN = {"id": 1, "priority": 1}
    CUSTOMER = {"id": 2, "priority": 2}
    NORMAL = {"priority": 3}

    @property
    def id(self):
        return self.value.get("id")

    def check_privileges(self, groups, exact=False):
        user_priority = float(
            "inf"
        )  # Initialize with positive infinity
        value = self.value
        for group_id in groups:
            if group_id >= 0 and group_id <= 2:
                group = self._member_map_[
                    self._member_names_[group_id]
                ]
                if "priority" in group.value:
                    user_priority = min(
                        user_priority,
                        group.value["priority"],
                    )
        priority = min(
            user_priority,
            self.NORMAL.value.get("priority", float("inf")),
        )

        target_priority = value.get(
            "priority", float("inf")
        )

        if exact:
            return target_priority == priority
        else:
            return priority <= target_priority
