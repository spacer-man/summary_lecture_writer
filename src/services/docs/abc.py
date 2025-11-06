from typing import Protocol


class DocsService(Protocol):
    """Service for forming documents"""
    async def new_doc(self, text: str) -> bytes:
        """
        Args:
            :text: str  # text that document should be contain
        Return:
            :doc: bytes # formed document
        """
        ...
