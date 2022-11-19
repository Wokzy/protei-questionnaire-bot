import yaml
import pickle
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
		with open(filename, 'r', encoding='utf-16') as f:
			prev_stats = yaml.safe_load(f)
			f.close()
	except FileNotFoundError:
		prev_stats = {}

	res = {}

	for i in data:
		if i not in ['Name', 'status', 'state']:
			res[i] = data[i]

	prev_stats[data['Name']] = res

	with open(filename, 'w') as f:
		yaml.dump(prev_stats, f)
