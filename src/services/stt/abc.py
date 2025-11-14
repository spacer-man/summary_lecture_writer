from typing import Protocol, BinaryIO

import numpy as np


class STTService(Protocol):
    """Speech to text recognising service"""
    async def recognise(self, audio: np.ndarray | BinaryIO) -> str:
        """
        Args:
            :audio: np.ndarray | BinaryIO  # audio for STT recognising
        Return:
            :recognised: str    # recognised text
        """
        ...
