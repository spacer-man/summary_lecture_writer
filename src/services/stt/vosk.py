from typing import BinaryIO

import numpy as np
from vosk import BatchModel
from vosk import BatchRecognizer
from vosk import GpuInit

from .abc import STTService


class VoskSTTService(STTService):
    """Speech to text recognising service implementated by vosk"""
    def __init__(self, model_path: str) -> None:
        GpuInit()
        self.model = BatchModel(model_path=model_path)

    async def recognise(self, audio: np.ndarray | BinaryIO) -> str:
        """
        Args:
            :audio: np.ndarray | BinaryIO  # audio for STT recognising
        Return:
            :recognised: str    # recognised text
        """
        if isinstance(audio, BinaryIO):
            audio = np.asarray(audio)

        recognizer = BatchRecognizer(self.model)
        recognizer.AcceptWaveform(audio)
        self.model.Wait()

        text = recognizer.Result()
        return text
