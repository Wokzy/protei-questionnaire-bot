import asyncio
import telegram

from utils import load_token

global TOKEN
TOKEN = load_token()


async def main():
	global TOKEN

	bot = telegram.Bot(TOKEN)
	async with bot:
		print(await bot.get_me())

if __name__ == '__main__':
	asyncio.run(main())
