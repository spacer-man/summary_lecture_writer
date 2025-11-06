from typing import Protocol


class SummariseService(Protocol):
    """Core service for summarisation"""
    async def summarise(self, text: str) -> str:
        """
        Args:
            :text: str  # text for summarisation
        Return:
            :summarised: str    # summarised text
        """
        ...
