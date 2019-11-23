import wallet_gen
import random
import os
import sys
import signal

MENU = '''------- Menu -------
1. Get random wallet
2. Upload wallet
3. Buy private token
4. Exit
> '''

FLAG = 'Cup{901caa40579a07ee5912514eebaf5526742ad03261971b233fd1cb88eee915ae}'
Current_Wallet = None

if __name__ == "__main__":
	signal.alarm( 10 )

	while 1:
		option = raw_input( MENU )

		if option == '1':
			username = wallet_gen.idg( random.randint( 16, 32 ) )
			password = wallet_gen.idg( random.randint( 32, 64 ) )

			wallet = wallet_gen.Wallet( username, password, 'Default' )
			tmp_filename = username
			wallet.pack_file( tmp_filename )
			
			buf = open( tmp_filename, 'rb' ).read()
			
			print buf.encode( 'hex' )

			os.system( "rm " + tmp_filename )

			answer =  raw_input( "[?] Set this wallet as your current wallet? [Y\\N] " )

			if answer.strip() == 'Y':
				Current_Wallet = wallet


		elif option == '2':
			data = raw_input( "Enter hex encoded wallet and press Enter: " )

			try:
				data = data.strip().decode( 'hex' )
			except:
				print '[-] Error in data parsing! Try again!'
				continue

			login = raw_input( 'Enter login: ' ).strip()
			password = raw_input( 'Enter password: ' ).strip()

			res = wallet_gen.DecryptWallet( data, login, password )

			if res == wallet_gen.FORMAT_FILE_ERROR:
				sys.exit( -1 )

			if res != wallet_gen.INCORRECT_LOGIN and res != wallet_gen.INCORRECT_PASSWORD:
				print "[+] Username and Passwrod is correct!"

			wallet_username, wallet_pass, wallet_info, wallet_balance, wallet_operations = res

			answer = raw_input( "[?] Set this wallet as your current wallet? [Y\\N] " )

			if answer.strip() == 'Y':
				Current_Wallet = wallet_gen.Wallet( wallet_username, wallet_pass, wallet_info )
				Current_Wallet.balance = wallet_balance
				Current_Wallet.last_operations = wallet_operations

		elif option == '3':
			if Current_Wallet == None:
				print "[-] Current wallet is not set!"
				continue

			if Current_Wallet.balance < 13371337:
				print "[-] Not enough money!"
				print "[-] Needed 13371337 arbacoins!"
				print "[-] You have %d arbacoins" % Current_Wallet.balance
				continue

			if len( Current_Wallet.last_operations ) <= 16:
				print "[-] You need more as 16 last operations!"
				continue

			if Current_Wallet.info != 'Private':
				print "[-] You needed private status in wallet info!"
				print "[-] Get wallet with word 'Private' in info field!"
				continue

			print "[+] Wallet is correct, here are you private token: ", FLAG

		elif option == '4':
			sys.exit( -1 )

		else:
			print "[-] Incorrect option!"
			sys.exit( -1 )