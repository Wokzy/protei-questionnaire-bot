import pickle
import ruamel.yaml as yaml

from constants import *


def load_token(filename = TOKEN_FILENAME):
	with open(filename, 'r') as f:
		TOKEN = f.read()
		f.close()

	return TOKEN


def dump_users_cache(cache, filename = USERS_CACHE_FILENAME):
	with open(filename, 'wb') as f:
		pickle.dump(cache, f)
		f.close()


def load_users_cache(filename = USERS_CACHE_FILENAME):
	try:
		with open(filename, 'rb') as f:
			data = pickle.load(f)
			f.close()
	except FileNotFoundError:
		return {}

	return data


def save_result(data:list, filename = RESULT_FILENAME):
	try:
		with open(filename, 'r', encoding='utf-8') as f:
			prev_stats = yaml.load(f, yaml.RoundTripLoader) or {}
			f.close()
	except FileNotFoundError:
		prev_stats = {}

	res = {}

	for i in data:
		if i not in [MAIN_RESULT_KEY, 'status', 'state', 'id']:
			res[i] = data[i]

	prev_stats[data[MAIN_RESULT_KEY]] = res

	with open(filename, 'w', encoding='utf-8') as f:
		f.write(yaml.dump(prev_stats, Dumper=yaml.RoundTripDumper, allow_unicode=True))


def in_rules(data, cfg):
	match cfg['result_key']:
		case 'contacts':
			if not (data.startswith('@') and ' ' not in data) and not data.isnumeric():
				return False, 'Введите номер телефона или никнейм тг, начиная с @'

	return (True, )
