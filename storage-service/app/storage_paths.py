from pathlib import Path


class InvalidObjectKeyError(ValueError):
    pass


def resolve_storage_path(storage_root: str, account_id: str, object_key: str) -> tuple[Path, str]:
    normalized_key = Path("/" + object_key).as_posix().lstrip("/")

    if not normalized_key or normalized_key.startswith(".."):
        raise InvalidObjectKeyError("Invalid objectKey path.")

    account_root = Path(storage_root).resolve() / account_id
    absolute_path = (account_root / normalized_key).resolve()

    if absolute_path != account_root and account_root not in absolute_path.parents:
        raise InvalidObjectKeyError("Invalid objectKey path.")

    relative_path = f"{account_id}/{normalized_key}"
    return absolute_path, relative_path
