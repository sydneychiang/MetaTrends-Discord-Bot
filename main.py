import discord
import os
import random
import requests
import json
from keep_alive import keep_alive
import filter_content
from datetime import date, datetime
# from markyp_html import webpage
# from markyp_highlightjs import js, themes, highlight
import math
# from replit import db


client = discord.Client()
companies = ["Google", "Microsoft", "Discord", "Apple", "Tesla", "Uber", "Facebook", "Oracle", "IBM", "Intel", "Adobe", "Amazon", "Lyftly"]

elevatorpitch = ["Metatrends is an api-based content ranking and trend aggregation system.", "Please help us.", "Get your top trending content here!", "I'll intern for free."]

def get_date():
  # str = ""
  today = date.today()
  now = datetime.now()
  return today.strftime("%B %d, %Y")

def format_content(content):
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

def calculate_page_nums_left(lst, limit):
  pass


def put_lst_in_backticks(lst, limit):
  newstr = "```autohotkey\n"
  for i in range(len(lst[0:limit])):
    newstr += f"{str(i+1)}) {lst[i]}\n"
  newstr += f"\n\t{math.ceil((len(lst)-limit)/limit)} more page(s)"
  newstr += "\n\nSee the full list of today's top trending content at: https://metatrends.live"
  newstr += "\n```"
  return newstr

#how you register an event
@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  if message.content.startswith("$$$hello"):
    await message.channel.send("hello!")

  elif message.content.startswith("$$$elevator-pitch"):
    await message.channel.send(random.choice(elevatorpitch))

  elif message.content.startswith("$$$acquire"):
    await message.channel.send("We are currently acquiring {}.".format(random.choice(companies)))

  elif message.content == "$$$get":
    lst = get_trending_overview()
    limit = 15
    msg = await message.channel.send(f"The current top trending content: " + put_lst_in_backticks(lst, limit))
    await msg.add_reaction('⬅️')
    await msg.add_reaction('➡️')

  elif message.content.startswith("$$$get"):
    num = int(message.content.split()[1]) - 1
    lst = get_trending_list()
    specificContent = "```ini\n" + filter_content.format_content(lst[num]) + "```"
    msg = await message.channel.send(specificContent)
    await msg.add_reaction('🌐')


def update_overview(msg):
  print(msg.content)
  msgLst = msg.content.split("\n")
  start = int(msgLst[1].split(")")[0])
  end = int(msgLst[len(msgLst)-6].split(")")[0])
  print(start, end)
  return "changing! woo!"

@client.event
async def on_reaction_add(reaction, user):
  if (user.name != "MetaTrends Bot"):
    if reaction.emoji == '⬅️' and reaction.message.content.startswith('The current top trending content:'):
      # await reaction.message.channel.send("go back!")
      # reaction.message.content
      # reaction.message.content = update_overview(reaction.message)
      await reaction.message.edit(content=update_overview(reaction.message))
    elif reaction.emoji == '➡️' and reaction.message.content.startswith('The current top trending content:'):
      await reaction.message.channel.send("onward!")
    # await reaction.message.channel.send('{} has added {} to the message {}'.format(user.name, reaction.emoji, reaction.message.content))


@client.event
async def on_reaction_remove(reaction, user):
  if (user.name != "MetaTrends Bot"):
    await reaction.message.channel.send('{} has removed {} from the message {}'.format(user.name, reaction.emoji, reaction.message.content))

keep_alive()
client.run(os.getenv("TOKEN"))


