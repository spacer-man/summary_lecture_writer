from .abc import SummariseService


class TestSummariseService(SummariseService):
    """Test implementation of core service for summarisation"""
    async def summarise(self, text: str) -> str:
        """
        Args:
            :text: str  # text for summarisation
        Return:
            :str:   # summarised text
        """
        return text
