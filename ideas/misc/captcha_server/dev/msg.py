class Msg:

	SERVER_BANNER = '''
 #####     #    ######  #######  #####  #     #    #        #####  ####### ######  #     # ####### ######  
#     #   # #   #     #    #    #     # #     #   # #      #     # #       #     # #     # #       #     # 
#        #   #  #     #    #    #       #     #  #   #     #       #       #     # #     # #       #     # 
#       #     # ######     #    #       ####### #     #     #####  #####   ######  #     # #####   ######  
#       ####### #          #    #       #     # #######          # #       #   #    #   #  #       #   #   
#     # #     # #          #    #     # #     # #     #    #     # #       #    #    # #   #       #    #  
 #####  #     # #          #     #####  #     # #     #     #####  ####### #     #    #    ####### #     # 
'''
	SERVER_RULES  = '1. The server sends you a captcha and you have 5 seconds to solve it\n'
	SERVER_RULES += '2. After solving a lot of captchas, we will reward you\n'

	SESSION_START = 'Do you want to start a captcha solution session? (Y/N): '

	EXIT = 'Close connection...\n'

	SERVER_AWARD  = 'Thank you for your help. This is a your award: '
	SERVER_AWARD += 'Cup{a6f6f28f15b85a6d0a2a0ae4c1460d97f5326f2cfe09fc1cf9ba663285bbca37}\n'
	ANSWER_MSG    = '\nAnswer: '
	SERVER_ANSWER_TIMEOUT = 'Time to solve is out!\n'
	CORRECT_CAPTCHA = '[+] Correct!\n'
	INCORRECT_CAPTHCA = "[-] Incorrect!\n"