import logging
from aiogram.utils import executor
from create_bot import dp
from user_handlers import user_handlers
from settings_handlers import settings_handlers
from commands_handlers import commands_handlers


logging.basicConfig(level=logging.DEBUG)


commands_handlers.register_commands_handlers(dp)
user_handlers.register_user_handlers(dp)
settings_handlers.register_settings_handlers(dp)


executor.start_polling(dp, skip_updates=True)
