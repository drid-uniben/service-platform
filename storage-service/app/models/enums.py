import enum


class ObjectStatus(str, enum.Enum):
    queued = "queued"
    stored = "stored"
    failed = "failed"


class FileVisibility(str, enum.Enum):
    private = "private"
    public = "public"

class AttemptStatus(str, enum.Enum):
    stored = "stored"
    failed = "failed"
