from AloneX import database2 as database

# Collections
db = database["imposter_chats"]
users_db = database["imposter_users"]

# Cache
IMPOSTER_CHATS = {}
USER_DATA = {}


async def impo_on(chat_id: int):
    if chat_id in IMPOSTER_CHATS:
        return True

    data = await db.find_one({"chat_id": chat_id})
    if data:
        IMPOSTER_CHATS[chat_id] = data
        return True

    doc = {
        "chat_id": chat_id,
        "enabled": True,
    }

    await db.insert_one(doc)
    IMPOSTER_CHATS[chat_id] = doc
    return False


async def impo_off(chat_id: int):
    if chat_id not in IMPOSTER_CHATS:
        data = await db.find_one({"chat_id": chat_id})
        if not data:
            return False

    await db.delete_one({"chat_id": chat_id})
    IMPOSTER_CHATS.pop(chat_id, None)
    return True


async def check_pretender(chat_id: int):
    if chat_id in IMPOSTER_CHATS:
        return True

    data = await db.find_one({"chat_id": chat_id})

    if data:
        IMPOSTER_CHATS[chat_id] = data
        return True

    return False


async def add_userdata(
    user_id: int,
    username=None,
    first_name=None,
    last_name=None,
):
    data = {
        "user_id": user_id,
        "username": username,
        "first_name": first_name,
        "last_name": last_name,
    }

    await users_db.update_one(
        {"user_id": user_id},
        {"$set": data},
        upsert=True,
    )

    USER_DATA[user_id] = data


async def usr_data(user_id: int):
    if user_id in USER_DATA:
        return USER_DATA[user_id]

    data = await users_db.find_one({"user_id": user_id})

    if data:
        USER_DATA[user_id] = data

    return data


async def get_userdata(user_id: int):
    data = await usr_data(user_id)

    if not data:
        return None, None, None

    return (
        data.get("username"),
        data.get("first_name"),
        data.get("last_name"),
    )


async def initialize_imposter():
    try:
        async for doc in db.find({}):
            IMPOSTER_CHATS[doc["chat_id"]] = doc

        async for doc in users_db.find({}):
            USER_DATA[doc["user_id"]] = doc
    except Exception:
        pass


async def reset_imposter(chat_id: int):
    await db.delete_one({"chat_id": chat_id})
    IMPOSTER_CHATS.pop(chat_id, None)


async def reset_userdata(user_id: int):
    await users_db.delete_one({"user_id": user_id})
    USER_DATA.pop(user_id, None)
