import datetime
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, func


class SoftDeleteMixin:
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    deleted_at = Column(DateTime, nullable=True)

    def soft_delete(self):
        self.deleted_at = datetime.datetime.utcnow()

    @property
    def is_deleted(self):
        return self.deleted_at is not None
