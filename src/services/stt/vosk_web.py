import logging
import wave
import websockets
from io import BytesIO

from pydantic import BaseModel

from .abc import STTService
from .exceptions import RecognizedError


log = logging.getLogger(__name__)


class Recognized(BaseModel):
    text: str

    model_config = {"extra": "allow"}


class VoskWebSTTService(STTService):
    """Speech to text recognising service implementated by vosk"""
    def __init__(
            self,
            url: str,
            ) -> None:
        self.url = url

    async def recognise(self, audio: BytesIO) -> str:
        """
        Args:
            :audio: BytesIO     # audio for STT recognising
        Return:
            :str:    # recognised text
        """
        recognized_text = ""
        if len(audio.getvalue()) == 0:
            return recognized_text
        audio.seek(0)

        try:
            async with websockets.connect(self.url) as websocket:
                    wf = wave.open(audio, "rb")
                    await websocket.send(
                        message='{ "config" : { "sample_rate" : %d } }' %
                        (wf.getframerate()))
                    buffer_size = int(wf.getframerate() * 0.2) # 0.2 seconds of audio
                    while True:
                        data = wf.readframes(buffer_size)

                        if len(data) == 0:
                            break

                        await websocket.send(data)
                        response = await websocket.recv(decode=True)
                        try:
                            recognized = Recognized.model_validate_json(response)
                        except Exception:
                            pass
                        else:
                            recognized_text += ' ' + recognized.text

                    await websocket.send('{"eof" : 1}')
                    response = await websocket.recv(decode=True)
            recognized = Recognized.model_validate_json(response)
        except Exception as err:
            raise RecognizedError from err
        else:
            recognized_text += ' ' + recognized.text
            return recognized_text
