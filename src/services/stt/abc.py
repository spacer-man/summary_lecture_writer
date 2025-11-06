from typing import Protocol

import numpy as np


class STTService(Protocol):
    """Speech to text recognising service"""
    async def recognise(self, audio: np.ndarray | bytes) -> str:
        """
        Args:
            :audio: np.ndarray | bytes  # audio for STT recognising
        Return:
            :recognised: str    # recognised text
        """
        ...
