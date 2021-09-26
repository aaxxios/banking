import subprocess as sp
import botbank
import os

CMD = "cls" if os.name == 'nt' else 'clear'

bank = botbank.Bank()

def select():
	sp.call(CMD, shell=True)
	try:
		sel = input("1. Create Account\n2. Login Account\n3. Deposit\n4. Transfer Funds\n5. Logout\n6. Exit\n\n")
	except KeyboardInterrupt:
		print("Goodbye!")
		exit(1)
	if sel=='1':
		sp.call(CMD, shell=True)
		bank.create_account()
	elif sel=='2':
		sp.call(CMD, shell=True)
		bank.login()
		input("\n\npress enter to go back:")
	elif sel=='3':
		sp.call(CMD, shell=True)
		bank.deposit()
		input("\n\npress enter to go back:")
	elif sel=='4':
		sp.call(CMD, shell=True)
		bank.transfer()
		input("\n\npress enter to go back:")
	elif sel=='5':
		sp.call(CMD, shell=True)
		bank.logout()
		input("\n\nYour data has been deleted \npress enter to go back:")
	else:
		return 0;
	return 1;


while(select()):
	pass