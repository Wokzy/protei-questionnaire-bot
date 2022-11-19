import utils
import asyncio
import bot_functions as bf

from telegram import (
	KeyboardButton,
	KeyboardButtonPollType,
	Poll,
	ReplyKeyboardMarkup,
	ReplyKeyboardRemove,
	Update,
)

from telegram.constants import ParseMode
from questionnaire_functions import q_functions as qf
from telegram.ext import (
	Application,
	CommandHandler,
	ContextTypes,
	MessageHandler,
	PollAnswerHandler,
	PollHandler,
	filters,
)

global TOKEN, users_cache
TOKEN = utils.load_token()
users_cache = utils.load_users_cache() # {'user_id':data...}


async def process_qf(user, data, update, context: ContextTypes.DEFAULT_TYPE, chat_id=None):
	global users_cache

	if users_cache[user]['status'] != 'finished':
		users_cache[user] = await qf[users_cache[user]['status']](user_data = users_cache[user], update=update,
															recieved_data=data, context=context, chat_id=chat_id)
		utils.dump_users_cache(users_cache)

		if users_cache[user]['status'] == 'finished':
			utils.save_result(data=users_cache[user])
	else:
		await context.bot.send_message(update.message.chat.id, 'Вы уже заполнили анкету, чтобы сделать это снова, введи /start')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	global users_cache
	user = update.message.from_user.id

	#if user not in users_cache:
	await update.message.reply_text(
		"Привет! Спасибо за интерес к нашей компании. Более 20 лет ПРОТЕЙ производит ПО в сфере телекоммуникаций. "
		"Мы всегда рады новым сотрудникам, проходи опрос и, возможно, скоро ты станешь частью нашей команды!"
	)
	#else:
	#	await update.message.reply_text('Чтож, начнём сначала')

	users_cache[user] = {'status':0, 'state':'message'}

	await context.bot.send_message(chat_id=update.message.chat.id, text='ФИО')


async def receive_poll_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	"""Summarize a users poll vote"""
	answer = update.poll_answer
	answered_poll = context.bot_data[answer.poll_id]
	try:
		questions = answered_poll["questions"]
	# this means this poll answer update is from an old poll, we can't do our answering then
	except KeyError:
		return
	await process_qf(user=update.effective_user.id, data=[questions[i] for i in answer.option_ids], update=update, context=context, chat_id=answered_poll["chat_id"])
	#answered_poll["answers"] += 1
	#if answered_poll["answers"] == 1:
	await context.bot.stop_poll(answered_poll["chat_id"], answered_poll["message_id"])
	utils.dump_users_cache(users_cache)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	global users_cache
	user = update.message.from_user.id

	if users_cache[user]['state'] == 'poll':
		await context.bot.send_message(update.message.chat.id, 'Ответте на опросник')
	else:
		await process_qf(user=user, data=update.message.text, update=update, context=context, chat_id=update.message.chat.id)



def main():
	global TOKEN

	application = Application.builder().token(TOKEN).build()
	application.add_handler(CommandHandler("start", start))
	application.add_handler(MessageHandler(filters.TEXT, handle_message))
	application.add_handler(PollAnswerHandler(receive_poll_answer))
	#async with bot:
		#updates = await bot.get_updates()
		#print(updates[0])
		#for i in updates:
		#	print(i)
		#await bot.sendPoll(chat_id=1378906881, question='test_poll', 
		#					options=['hello', 'goo', '123'], is_anonymous=False)
	application.run_polling()

if __name__ == '__main__':
	#asyncio.run(main())
	main()
