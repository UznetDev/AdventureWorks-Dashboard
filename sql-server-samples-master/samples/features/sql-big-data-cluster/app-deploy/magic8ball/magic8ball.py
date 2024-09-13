#This is a sample Python Script for an implementation for magic8ball
import sys
import random
def magic8ball(txt):
    question = txt
    #print (input)
    answers = random.randint(1,8)
    msg=""
    if question == "":
        sys.exit()

    elif answers == 1:
        msg="It is certain"
	
    elif answers == 2:
        msg="Outlook good"

    elif answers == 3:
        msg="You may rely on it"

    elif answers == 4:
        msg="Ask again later"

    elif answers == 5:
        msg="Concentrate and ask again"

    elif answers == 6:
        msg="Reply hazy, try again"

    elif answers == 7:
        msg="My reply is no"

    elif answers == 8:
        msg="My sources say no"

    return msg
