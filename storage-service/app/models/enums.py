import enum


class ObjectStatus(enum.Enum):
    queued = "queued"
    stored = "stored"
    failed = "failed"

class AttemptStatus(enum.Enum):
    stored = "stored"
    failed = "failed"
