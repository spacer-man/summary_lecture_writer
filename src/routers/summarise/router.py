from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.types import Message
from aiogram.enums import ChatAction

from routers import messages as common_messages
from services.summarise.abc import SummariseService
from services.stt.abc import STTService


summarise_router = Router(name="summarise")


@summarise_router.message(StateFilter(None))
async def summarise_audio(
        message: Message,
        stt_service: STTService,
        summarise_service: SummariseService,
        ) -> None:
    if message.bot:
        await message.bot.send_chat_action(
                chat_id=message.chat.id,
                action=ChatAction.TYPING)
        if message.audio:
            audio_file_id = message.audio.file_id
        elif message.voice:
            audio_file_id = message.voice.file_id
        else:
            return None

        try:
            audio = await message.bot.download(audio_file_id)
            text_to_summarise = await stt_service.recognise(audio=audio)
            summarised_text = await summarise_service.summarise(
                text=text_to_summarise)
        except Exception:
            await message.answer(text=common_messages.UNKNOWN_INTERNAL_ERROR)
        else:
            await message.answer(text=summarised_text)
    else:
        await message.answer(text=common_messages.UNKNOWN_INTERNAL_ERROR)
