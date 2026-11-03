import asyncio
import logging
from config import bot, dp
from handlers import commands, echo, fsm_add_product, fsm_add_drink

dp.include_router(router=commands.router_commands)
dp.include_router(router=fsm_add_product.router_add_name)
dp.include_router(router=fsm_add_drink.router_add_title)
dp.include_router(router=echo.router_echo)



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(dp.start_polling(bot))

    