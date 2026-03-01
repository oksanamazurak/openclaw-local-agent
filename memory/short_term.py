
MAX_SHORT_TERM = 40


class ShortTermMemory:
    """Sliding-window conversation buffer."""

    def __init__(self, max_messages: int = MAX_SHORT_TERM):
        self.max_messages = max_messages
        self._messages: list = []

    def add(self, message) -> None:
        self._messages.append(message)
        if len(self._messages) > self.max_messages:
            self._messages = self._messages[-self.max_messages:]

    def add_many(self, messages: list) -> None:
        for m in messages:
            self.add(m)

    def get_messages(self) -> list:
        return list(self._messages)

    def clear(self) -> None:
        self._messages.clear()

    def to_dicts(self) -> list[dict]:
        return [
            {
                "role": getattr(m, "type", "unknown"),
                "content": getattr(m, "content", str(m)),
            }
            for m in self._messages
        ]
