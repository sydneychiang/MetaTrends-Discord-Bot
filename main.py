import discord
import os
import random
import requests
import json
from keep_alive import keep_alive
import filter_content
from datetime import date, datetime
import math

client = discord.Client()
companies = ["Google", "Microsoft", "Discord", "Apple", "Tesla", "Uber", "Facebook", "Oracle", "IBM", "Intel", "Adobe", "Amazon", "Lyftly"]

elevatorpitch = ["Metatrends is an api-based content ranking and trend aggregation system.", "Please help us.", "Get your top trending content here!", "I'll intern for free."]

def get_date():
  today = date.today()
  # now = datetime.now()
  return today.strftime("%B %d, %Y")

def format_content(content):
  if content["type"] == "twitch":
    return f"https://twitch.tv/{content['user_name']}"
  elif content["type"] == "reddit":
    return f"https://{content['link']}"
  else:
    return content["link"]


def get_trending_list():
  response = requests.get("https://metatrends.live/api/getRecentTrendingData")
  jsonData = json.loads(response.text)
  data = jsonData["data"]
  lst = [content for content in data]
  return lst

def get_trending_overview():
  requestedContent = get_trending_list()
  lst = []
  for i in range(len(requestedContent)):
    contentType, contentStr = filter_content.get_titles(requestedContent[i])
    if len(str(i+1)) + len(contentStr) > 50:
      contentStr = contentStr[0:50-len(str(i+1))] + "..."
    else:
      contentStr += ((53 - (len(str(i+1)) + len(contentStr))) * " ")
    lst.append(contentStr + "\t" + f"[{contentType.capitalize()}]")
  return lst

def calculate_page_nums_left(lst, end):
  return math.ceil((len(lst)-end)/15);

def put_lst_in_backticks(lst, start, end):
  newstr = "```autohotkey\n"
  for i in range(start, end):
    newstr += f"{str(i+1)}) {lst[i]}\n"
  newstr += f"\n\t{calculate_page_nums_left(lst, end)} more page(s)"
  newstr += "\n\nSee the full list of today's top trending content at: https://metatrends.live"
  newstr += "\n```"
  return newstr

def get_help_msg():
  msg = "My current available commands are:\n\n"
  msg += "$$$help - get available commands\n"
  msg += "$$$acquire - see what companies we are currently acquiring\n"
  msg += "$$$elevator-pitch - get the MetaTrend's creator's elevator pitches\n"
  msg += "$$$get - get an overview of today's top trending content\n"
  msg += "$$$get [num] - get detailed content on that number in the overview list"
  return msg

#how you register an event
@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if message.content == "$$$help":
    await message.channel.send(get_help_msg())
  elif message.content.startswith("$$$elevator-pitch"):
    await message.channel.send(random.choice(elevatorpitch))

  elif message.content.startswith("$$$acquire"):
    await message.channel.send("We are currently acquiring {}.".format(random.choice(companies)))

  elif message.content == "$$$get":
    lst = get_trending_overview()
    limit = 15
    msg = await message.channel.send(f"The current top trending content: " + put_lst_in_backticks(lst, 0, limit))
    await msg.add_reaction('⬅️')
    await msg.add_reaction('➡️')

  elif message.content.startswith("$$$get"):
    num = int(message.content.split()[1]) - 1
    lst = get_trending_list()
    specificContent = "```ini\n" + filter_content.format_content(lst[num]) + "```"
    msg = await message.channel.send(specificContent)
    await message.channel.send(format_content(lst[num]))
    # await msg.add_reaction('🌐')

def calculate_indices(lst, start, end, isForward):
  if isForward:
    start = end
    end = len(lst) if end+15 > len(lst)-1 else end+15
  else:
    end = start
    start = 0 if start-15 < 0 else start-15 
  return start, end

def update_overview(msg, isForward):
  msgLst = msg.content.split("\n")
  start = int(msgLst[1].split(")")[0]) - 1
  end = int(msgLst[len(msgLst)-6].split(")")[0])
  lst = get_trending_list()

  if (start == 0 and not isForward) or (end == len(lst) and isForward):
    return msg.content

  newstart, newend = calculate_indices(lst, start, end, isForward)
  newstr = put_lst_in_backticks(get_trending_overview(), newstart, newend)

  return 'The current top trending content:' + newstr

@client.event
async def on_reaction_add(reaction, user):
  if (user.name != "MetaTrends Bot"):
    if reaction.emoji == '⬅️' and reaction.message.content.startswith('The current top trending content:'):
      await reaction.message.edit(content=update_overview(reaction.message, False))
      await reaction.message.remove_reaction(reaction.emoji, user)

    elif reaction.emoji == '➡️' and reaction.message.content.startswith('The current top trending content:'):
      await reaction.message.edit(content=update_overview(reaction.message, True))
      await reaction.message.remove_reaction(reaction.emoji, user)


keep_alive()
client.run(os.getenv("TOKEN"))


