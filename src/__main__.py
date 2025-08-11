
import asyncio

from src import bot, dp, log

async def main():
    # resolve used update types
    useful_updates = dp.resolve_used_update_types()
    await dp.start_polling(bot, allowed_updates=useful_updates)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        log.info("bot stopped!")