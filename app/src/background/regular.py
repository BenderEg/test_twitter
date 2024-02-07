from datetime import datetime
from json import dumps
from uuid import UUID

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from core.config import settings
from core.logger import logging
from db.red_conn import get_redis
from db.sqlalcem import async_session
from external.feed_repository import FeedRepository
from external.user_repository import UserRepository

scheduler = AsyncIOScheduler()

async def send_twits_to_users():
    redis = await get_redis()
    async with async_session() as session:
        feed_repo = FeedRepository(session)
        user_repo = UserRepository(session)
        today = datetime.utcnow().date().isoformat()
        logging.info(f"Starting daily notifications on {today}")
        last_processed_user = await redis.get(today)
        if last_processed_user:
            last_processed_user = UUID(last_processed_user)
        users_ids = await user_repo.get_users_id_in_partitions(last_processed_user)
        for partition in users_ids:
            feeds = await feed_repo.get_feeds(partition, settings.twit_numbers)
            for ele in feeds:
                user_id = ele[0]
                twits = "\n".join([dumps(
                    {"author_id": str(value[0]),
                     "header": value[1],
                     "content":value[2],
                     "creation_date": value[3].isoformat()
                    }) for value in ele[1]])
                logging.warning(f"\nSend to user: {user_id}\nTwits:\n{twits}")
            await redis.set(name=today, value=str(partition[-1]), ex=60*60*24)
        logging.info(f"Finish daily notifications on {today}")


async def clean_feed_table():
    async with async_session() as session:
        feed_repo = FeedRepository(session)
        logging.info(f"Starting feed table cleaning")
        await feed_repo.clean_feeds_table(settings.max_twits)
        logging.info(f"Finish feed table cleaning")

scheduler.add_job(clean_feed_table, "interval", seconds=5)