from __future__ import annotations


class HeliconeProvider:
    """
    Stub provider.
    Implement actual Helicone integration in a project that needs it, keeping secrets out of git.
    """

    def __init__(self) -> None:
        self.enabled = False

    def is_enabled(self) -> bool:
        return self.enabled

