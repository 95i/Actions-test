import argparse
import telegram


parser = argparse.ArgumentParser(description="Demo of argparse")
parser.add_argument('-token','--token', default=' 5 ')
# parser.add_argument('-y','--year', default='20')
args = parser.parse_args()
# print(args)
a = args.token
# b = args.year

# print(type(a))
# print(a+b)
print(a)
bot = telegram.Bot(token=a)
bot.send_message(chat_id='-405240242', text="00000")
