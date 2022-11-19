import bot_functions as bf

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

async def finish(user_data, recieved_data, update, context, chat_id):
	user_data['status'] = 'finished'
	user_data['course'] = recieved_data

	user_data['state'] = 'message'
	await context.bot.send_message(chat_id, 'До встречи!')

	return user_data


q_functions = [get_bio, get_contacts, get_user_occupation_direction, get_users_favourite_from_studies, finish] #{0:get_bio, get_contacts}
