import bot_functions as bf
from constants import MAIN_RESULT_KEY, questions_sequence


__author__ = 'Yegor Yershov'



async def finish(user_data, context, chat_id):
	user_data['status'] = 'finished'

	user_data['state'] = 'message'
	await context.bot.send_message(chat_id, 'До встречи!')

	print(f'{user_data[MAIN_RESULT_KEY]} [{user_data["id"]}] Has just finished!')

	return user_data


async def start(context, chat_id):
	await context.bot.send_message(chat_id=chat_id, text=questions_sequence[0]['text'])
	return {'status':0, 'state':'message'}


async def struct_info(user_data, recieved_data, update, context, chat_id):

	user_data[questions_sequence[user_data['status']]['result_key']] = recieved_data
	user_data['status'] += 1

	if user_data['status'] >= len(questions_sequence):
		return await finish(user_data, context, chat_id)

	question = questions_sequence[user_data['status']]
	user_data['state'] = question['type']

	if question['type'] == 'message':
		await context.bot.send_message(chat_id, question['text'])
	elif question['type'] == 'markup':
		await bf.markup(chat_id, context, answers=question['answers'], question=question['question'])

	return user_data
