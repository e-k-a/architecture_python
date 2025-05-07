import redis.asyncio as redis
import json
from settings import settings

redis_client = redis.Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    decode_responses=True,
)

CACHE_EXPIRE_SECONDS = 120 

async def get_cached_user(user_id: int):
    try:
        data = await redis_client.get(f"user:{user_id}")
        if data:
            return json.loads(data)  
        return None
    except Exception as e:
        print(f"Error fetching from cache for user {user_id}: {e}")
        return None

async def set_cached_user(user_id: int, user_data: dict):
    try:
        await redis_client.setex(
            f"user:{user_id}", CACHE_EXPIRE_SECONDS, json.dumps(user_data)
        )
    except Exception as e:
        print(f"Error setting cache for user {user_id}: {e}")
