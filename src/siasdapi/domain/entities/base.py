from dataclasses import asdict
from datetime import datetime


class BaseEntity:
    @classmethod
    def from_dict(cls, dict_):
        return cls(**dict_)

    def to_dict(self):
        return asdict(self)

    def soft_delete(self):
        if hasattr(self.Meta, "active_field"):
            active_field = self.Meta.active_field
            setattr(self, active_field, False)
        if hasattr(self, "deleted_at"):
            self.deleted_at = datetime.now()
        if hasattr(self, "updated_at"):
            self.updated_at = datetime.now()

    def recover(self):
        if hasattr(self.Meta, "active_field"):
            active_field = self.Meta.active_field
            setattr(self, active_field, True)
        if hasattr(self, "deleted_at"):
            self.deleted_at = None
        if hasattr(self, "updated_at"):
            self.updated_at = datetime.now()
