import logging
import wave
from io import BytesIO

from pydantic import BaseModel
from vosk import Model
from vosk import KaldiRecognizer
from vosk import SetLogLevel

from .abc import STTService
from .exceptions import RecognizedError


log = logging.getLogger(__name__)


class Recognized(BaseModel):
    text: str

    model_config = {"extra": "allow"}


class VoskKaldiSTTService(STTService):
    """Speech to text recognising service implementated by vosk"""
    def __init__(
            self,
            model_path: str,
            log_level: int = logging.WARNING,
            ) -> None:
        SetLogLevel(log_level)

        self.model_path = model_path

    async def recognise(self, audio: BytesIO) -> str:
        """
        Args:
            :audio: BytesIO     # audio for STT recognising
        Return:
            :str:    # recognised text
        """
        if len(audio.getvalue()) == 0:
            return ""
        audio.seek(0)

        try:
            model = Model(model_path=self.model_path)
            wf = wave.open(audio, "rb")

            recognizer = KaldiRecognizer(model, wf.getframerate())
            recognizer.SetWords(True)
            recognizer.SetPartialWords(True)

            while True:
                data = wf.readframes(16_000)

                if len(data) == 0:
                    break

                if recognizer.AcceptWaveform(data=data):
                    recognizer.Result()
                else:
                    recognizer.PartialResult()

            recognized = recognizer.FinalResult()

            if isinstance(recognized, str):
                result = Recognized.model_validate_json(recognized)
            else:
                result = Recognized.model_validate(recognized)
        except Exception as err:
            raise RecognizedError from err
        else:
            return result.text
