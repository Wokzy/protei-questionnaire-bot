

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
