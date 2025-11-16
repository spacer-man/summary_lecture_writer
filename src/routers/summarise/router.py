import logging
from io import BytesIO

from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.types import Message
from aiogram.enums import ChatAction

from lib.audio_converter import AudioConverter
from routers import messages as common_messages
from routers.filters import IsRegisteredFilter
from routers.summarise import messages
from services.summarise.abc import SummariseService
from services.stt.abc import STTService
from services.stt.exceptions import RecognizedError


summarise_router = Router(name="summarise")
log = logging.getLogger(__name__)


@summarise_router.message(StateFilter(None), IsRegisteredFilter(True))
async def summarise_audio(
        message: Message,
        stt_service: STTService,
        summarise_service: SummariseService,
        ) -> None:
    user_telegram_id = message.chat.id
    event_id = message.message_id

    if message.bot:
        await message.answer(text=messages.PROCESSING)
        await message.bot.send_chat_action(
                chat_id=user_telegram_id,
                action=ChatAction.TYPING)
        if message.audio:
            audio_file_id = message.audio.file_id
        elif message.voice:
            audio_file_id = message.voice.file_id
        else:
            return None

        log.debug({
            "event_id": event_id,
            "message": "Start downloading audio",
            "telegram_id": user_telegram_id,
            "file_id": audio_file_id,
        })
        try:
            opus_audio = BytesIO()
            await message.bot.download(
                file=audio_file_id,
                destination=opus_audio)
            log.debug({
                "event_id": event_id,
                "message": "Start recognising speech from audio",
                "telegram_id": user_telegram_id,
                "file_id": audio_file_id,
            })
            wav_audio = AudioConverter.opus_to_wav(origins=opus_audio)

            text_to_summarise = await stt_service.recognise(audio=wav_audio)
            if len(text_to_summarise) == 0:
                raise ValueError("Text to summarise should be not empty")

            log.debug({
                "event_id": event_id,
                "message": "Start summarising text",
                "telegram_id": user_telegram_id,
            })
            summarised_text = await summarise_service.summarise(
                text=text_to_summarise)
        except RecognizedError as err:
            await message.answer(text=messages.RECOGNIZING_ERROR)
            log.error({
                "event_id": event_id,
                "message": "Error at recognizing: %r",
                "telegram_id": user_telegram_id,
            }, err, exc_info=True)
        except ValueError as err:
            await message.answer(text=messages.EMPTY_RECOGNIZED_ERROR)
            log.error({
                "event_id": event_id,
                "message": "Error at recognizing: %r",
                "telegram_id": user_telegram_id,
            }, err, exc_info=True)
        except Exception as err:
            await message.answer(text=common_messages.UNKNOWN_INTERNAL_ERROR)
            log.error({
                "event_id": event_id,
                "message": "Error at summarising: %r",
                "telegram_id": user_telegram_id,
            }, err, exc_info=True)
        else:
            log.debug({
                "event_id": event_id,
                "message": "Successful summarised audio",
                "telegram_id": user_telegram_id,
            })
            await message.reply(text=summarised_text)
    else:
        await message.answer(text=common_messages.UNKNOWN_INTERNAL_ERROR)
        log.error({
            "event_id": event_id,
            "message": "Error at summarise_audio handler: message.bot is %r",
            "telegram_id": user_telegram_id,
        }, message.bot, exc_info=True)
