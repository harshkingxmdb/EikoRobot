import asyncio
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped

from AloneX import app, logger

# 🔥 GLOBAL PLAYER
call_py = PyTgCalls(app)

# 🎵 ACTIVE CALLS TRACK
active_calls = {}


# ---------------- JOIN VC ---------------- #

async def join_vc(chat_id: int):
    try:
        await call_py.join_group_call(
            chat_id,
            MediaStream(
                AudioPiped("silence.mp3")  # dummy file
            ),
        )
        active_calls[chat_id] = True
        return True
    except Exception as e:
        logger.error(f"VC join failed: {e}")
        return False


# ---------------- PLAY AUDIO ---------------- #

async def play_audio(chat_id: int, file_path: str):
    try:
        await call_py.change_stream(
            chat_id,
            MediaStream(
                AudioPiped(file_path)
            ),
        )
        return True
    except Exception as e:
        logger.error(f"Audio play failed: {e}")
        return False


# ---------------- PLAY VIDEO ---------------- #

async def play_video(chat_id: int, file_path: str):
    try:
        await call_py.change_stream(
            chat_id,
            MediaStream(
                AudioVideoPiped(file_path)
            ),
        )
        return True
    except Exception as e:
        logger.error(f"Video play failed: {e}")
        return False


# ---------------- STOP ---------------- #

async def stop_stream(chat_id: int):
    try:
        await call_py.leave_group_call(chat_id)
        active_calls.pop(chat_id, None)
        return True
    except Exception as e:
        logger.error(f"Stop failed: {e}")
        return False


# ---------------- PAUSE ---------------- #

async def pause_stream(chat_id: int):
    try:
        await call_py.pause_stream(chat_id)
        return True
    except Exception as e:
        logger.error(f"Pause failed: {e}")
        return False


# ---------------- RESUME ---------------- #

async def resume_stream(chat_id: int):
    try:
        await call_py.resume_stream(chat_id)
        return True
    except Exception as e:
        logger.error(f"Resume failed: {e}")
        return False


# ---------------- SKIP ---------------- #

async def skip_stream(chat_id: int):
    try:
        # queue system handle karega next
        return True
    except Exception as e:
        logger.error(f"Skip failed: {e}")
        return False


# ---------------- START CLIENT ---------------- #

async def start_player():
    await call_py.start()
