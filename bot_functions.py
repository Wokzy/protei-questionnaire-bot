from telegram import ReplyKeyboardMarkup

__author__ = 'Yegor Yershov'

async def poll(chat_id, context, answers, question, allows_multiple_answers=False) -> None:
	message = await context.bot.send_poll(
		chat_id,
		question,
		answers,
		is_anonymous=False,
		allows_multiple_answers=allows_multiple_answers
	)
	# Save some info about the poll the bot_data for later use in receive_poll_answer
	payload = {
		message.poll.id: {
			"questions": answers,
			"message_id": message.message_id,
			"chat_id": chat_id,
			"allows_multiple_answers":allows_multiple_answers,
			"answers": 0,
		}
	}
	context.bot_data.update(payload)


async def markup(chat_id, context, answers:list, question:str): # answers is list containing lists
	#markup_buttons = [[string] for string in answers]

	message = await context.bot.send_message(chat_id=chat_id, text=question, 
											reply_markup=ReplyKeyboardMarkup(answers, one_time_keyboard=True))

	string_answers = []
	for lst in answers:
		string_answers += lst


	payload = {
			"answers": string_answers,
			"message_id": message.message_id,
			"chat_id": chat_id,
			}

	context.bot_data.update(payload)
