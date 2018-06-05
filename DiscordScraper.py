from values import *
import discord
import asyncio
import csv
import re
from datetime import datetime
from datetime import timedelta
from toxicitythreat.perspective import toxicity

client = discord.Client()

admin_ids = [ADMIN_ID]	#currently, it only works with one admin id.
									#It will be changed in the future to support messaging multiple people
									
									
									

#helper function for parseIntroduction
#removes any consecutive whitespace characters and replaces them with a new line		
def removeTrailingWhitespace(text):
	pattern = re.compile(r'([ ]+)\s')
	return str(pattern.sub('\n', text))

	
	
	
#logs a message from all channels except those in the blacklist
def logMessage(message, introduction):

	#logs data to introduction.csv if it comes from the introduction channel
	if message.channel.id == introduction:
		intro_data = (messages.author.id, str(message.timestamp), message.clean_content.replace("\n" , " "))
		intro_writer.writerow(intro_data)
			
	#logs data from all other channels to messages.csv
	else:
		roles = [r.name for r in message.author.roles[1:]]		
		messageInfo = (roles, str(message.timestamp), message.channel.name, message.clean_content, message.author.id, toxicity(message.clean_content) )#NOTE: @here and @everyone mentions include the unicode zero width space for whatever reason
		print (messageInfo)
		csvwriter.writerow(messageInfo)

		
		
		
		
		
		
		
#messages people in the admin_ids list with the specified message, then closes the client	
async def messageAdmins(message):
	admins = []
	for id in admin_ids:
		a = await client.get_user_info(id)
		admins.append(a)
		
	for admin in admins:
		await client.send_message(admin, message)	
		
		
		
async def writeOldIntroIds():
	channel_id = '247264977495392258'
	first_message_id = '336899787502780427'
	
	channel = get_channel(channel_id)
	first_message = get_message(channel=channel, id=first_message_id)
	async for message in client.logs_from(channel, limit=1000):
		intro_data = (messages.author.id, str(message.timestamp), message.clean_content.replace("\n" , " "))
		intro_writer.writerow(intro_data)
	
		
#on startup
@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')
	await client.change_presence(status=discord.Status.invisible) 

#when a message is sent or received
@client.event
async def on_message(message):
	global last_reminder
	if message.timestamp - last_reminder > timedelta(days=1):
		last_reminder = message.timestamp
		await messageAdmins("The bot is still up! - " + str(last_reminder))
	try:
		if message.clean_content == 'X_!Pga@pdCHHDzGnpGY5V-!mGL&&aDfF':
			await writeOldIntroIds()
		elif type(message.author) == discord.Member:
			logMessage(message, INTRODUCTION_ID)
	except:
		print('There was an error somewhere.\n Message id: ' + message.id)
#		await messageAdmins('There was an error somewhere.\n Message id: ' + message.id)
	
		
		

#opens files to be written to
intro_file = open('introductions_v2.csv', 'a')
intro_writer = csv.writer(intro_file)
print('opened introductions_v2.csv to append')

message_file = open("messages.csv", 'a')
csvwriter = csv.writer(message_file)
print("Opened messages.csv to append")
last_reminder = datetime.now()
 
client.run(BOT_ID)