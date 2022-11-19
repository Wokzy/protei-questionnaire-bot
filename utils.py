

def load_token(filename = 'token.txt'):
	with open(filename, 'r') as f:
		TOKEN = f.read()
		f.close()

	return TOKEN
