import logging

from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.types import Message
from aiogram.enums import ChatAction

from routers import messages as common_messages
from routers.filters import IsRegisteredFilter
from services.summarise.abc import SummariseService
from services.stt.abc import STTService


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
            audio = await message.bot.download(audio_file_id)
            log.debug({
                "event_id": event_id,
                "message": "Start recognising speech from audio",
                "telegram_id": user_telegram_id,
                "file_id": audio_file_id,
            })
            assert audio is not None, "Audio should be not None"
            text_to_summarise = await stt_service.recognise(audio=audio)
            log.debug({
                "event_id": event_id,
                "message": "Start summarising text",
                "telegram_id": user_telegram_id,
            })
            summarised_text = await summarise_service.summarise(
                text=text_to_summarise)
        except Exception as err:
            await message.answer(text=common_messages.UNKNOWN_INTERNAL_ERROR)
            log.error({
                "event_id": event_id,
                "message": "Error while summarising: %r",
                "telegram_id": user_telegram_id,
            }, err)
        else:
            log.debug({
                "event_id": event_id,
                "message": "Successful summarised audio",
                "telegram_id": user_telegram_id,
            })
            await message.answer(text=summarised_text)
    else:
        await message.answer(text=common_messages.UNKNOWN_INTERNAL_ERROR)
        log.error({
            "event_id": event_id,
            "message": "Error while summarising: message.bot is %r",
            "telegram_id": user_telegram_id,
        }, message.bot)
