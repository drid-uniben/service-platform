import time


class InMemoryRateLimiter:
    def __init__(self) -> None:
        self._counter: dict[str, int] = {}

    def is_allowed(self, key: str, max_per_minute: int) -> bool:
        if max_per_minute <= 0:
            return True

        minute_bucket = int(time.time() // 60)
        bucket_key = f"{key}:{minute_bucket}"
        current = self._counter.get(bucket_key, 0)
        next_value = current + 1
        self._counter[bucket_key] = next_value

        oldest_allowed_bucket = minute_bucket - 2
        if len(self._counter) > 500:
            self._counter = {
                existing_key: value
                for existing_key, value in self._counter.items()
                if int(existing_key.rsplit(":", 1)[1]) >= oldest_allowed_bucket
            }

        return next_value <= max_per_minute
