from io import BytesIO
from typing import Protocol


class STTService(Protocol):
    """Speech to text recognising service"""
    async def recognise(
            self,
            audio: BytesIO,
            ) -> str:
        """
        Args:
            :audio: BytesIO     # audio for STT recognising
        Return:
            :str:   # recognised text
        """
        ...
