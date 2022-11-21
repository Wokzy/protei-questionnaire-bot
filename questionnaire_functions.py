import bot_functions as bf
from constants import MAIN_RESULT_KEY


__author__ = 'Yegor Yershov'


global questions_sequence
questions_sequence = \
[
{'type':'message', 'text':'ФИО', 'result_key':MAIN_RESULT_KEY},
{'type':'message', 'text':'Твой контакт для связи (тел, тг)', 'result_key':'contacts'},
{'type':'poll', 'question':'Хотел бы в будущем работать по специальности?', 'answers':['ДА', 'НЕТ'], 'result_key':'occupation_connected_with_speciality'},
{'type':'message', 'text':'Что из изученного по программе тебе понравилось больше всего? Почему?', 'result_key':'users_favourite_from_studies'},
{'type':'poll', 'question':'Курс?', 'answers':['1', '2', '3', '4', '5', 'Магистратура', 'Аспирантура'], 'result_key':'course'},#, 'allows_multiple_answers':False},
]


async def finish(user_data, context, chat_id):
	user_data['status'] = 'finished'

	user_data['state'] = 'message'
	await context.bot.send_message(chat_id, 'До встречи!')

	return user_data


async def struct_info(user_data, recieved_data, update, context, chat_id):
	'''
	if user_data['status'] == 'finished':
		await context.bot.send_message(chat_id, 'Вы уже заполнили анкету, чтобы сделать это снова, введите /start')
		return user_data
	'''

	user_data[questions_sequence[user_data['status']]['result_key']] = recieved_data
	user_data['status'] += 1

	if user_data['status'] >= len(questions_sequence):
		return await finish(user_data, context, chat_id)

	question = questions_sequence[user_data['status']]
	user_data['state'] = question['type']

	if question['type'] == 'message':
		await context.bot.send_message(chat_id, question['text'])
	elif question['type'] == 'poll':
		#TODO replace poll on buttons
		if 'allows_multiple_answers' not in question:
			question['allows_multiple_answers'] = False
		await bf.poll(update, context, answers=question['answers'], question=question['question'], allows_multiple_answers=question['allows_multiple_answers'])

	return user_data


'''
async def get_bio(user_data, recieved_data, update, context, chat_id):
	user_data['status'] += 1
	user_data['Name'] = recieved_data

	user_data['state'] = 'message'
	await context.bot.send_message(chat_id, 'Твой контакт для связи (тел, тг)')

	return user_data


async def get_contacts(user_data, recieved_data, update, context, chat_id):
	user_data['status'] += 1
	user_data['contacts'] = recieved_data


	answers = ['ДА', 'НЕТ']
	question = 'Хотел бы в будущем работать по специальности?'

	user_data['state'] = 'poll'
	await bf.poll(update, context, answers=answers, question=question)

	return user_data


async def get_user_occupation_direction(user_data, recieved_data, update, context, chat_id):
	user_data['status'] += 1
	user_data['user_would_like_to_have_an_occupation_connected_with_speciality'] = recieved_data

	user_data['state'] = 'message'
	await context.bot.send_message(chat_id, 'Что из изученного по программе тебе понравилось больше всего? Почему?')

	return user_data


async def get_users_favourite_from_studies(user_data, recieved_data, update, context, chat_id):
	user_data['status'] += 1
	user_data['users_favourite_from_studies'] = recieved_data


	answers = ['1', '2', '3', '4', '5', 'Магистратура', 'Аспирантура']
	question = 'Курс'

	user_data['state'] = 'poll'
	await bf.poll(update, context, answers=answers, question=question, allows_multiple_answers=True)

	return user_data
'''


#q_functions = [get_bio, get_contacts, get_user_occupation_direction, get_users_favourite_from_studies, finish] #{0:get_bio, get_contacts}
