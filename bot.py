import nest_asyncio
nest_asyncio.apply()

import pickle
import discord, os, traceback, asyncio, random
from discord.ext import tasks

from flask import Flask
from threading import Thread

from itertools import cycle

bowing_server_guild_id = 948183518511509545
active_channel_id = 948183518511509548
bot_owner_id = 568446269610000385
words, swear_words = [], []
swear_check_free_channels = [] # ids


app = Flask('')

@app.route('/')
def main():
  return "Your Bot Is Ready"

def run():
  app.run(host="0.0.0.0", port=8000)

def keep_alive():
  server = Thread(target=run)
  server.start()



intents = discord.Intents(guilds = True, dm_messages = True, members = True, messages = True, guild_messages = True, invites = True, message_content = True)
client = discord.Client(chunk_guilds_at_startup = True, intents = intents)

status = cycle(['Bowing the hell out of whoever calls me to their server and bawn bowing...','Bowing the hell out of whoever calls me to their server and bawn bowing....'])



def load_words() :
  global words, swear_words

  try :
    with open('words.txt') as f :
        words = f.read().split('\n')
        pass
    print('Words loaded to the list successfully.')
  except :
    print('Words failed to be loaded.')

  try :
    with open('swear_words1.txt') as f1 :
      swear_words1 = f1.read().split('\n')
      with open('swear_words2.txt') as f2 :
        swear_words2 = f2.read().split('\n')
        swear_words = swear_words1.copy() + [word for word in swear_words2 if word not in swear_words1].copy()
    print('Swear words loaded to the list successfully.')
  except :
    print('Swear words failed to be loaded.')
  return

def load_swear_check_free_channels() :
  global swear_check_free_channels

  try :
    with open('swear_free_channels.bin', 'rb') as f :
      swear_check_free_channels = pickle.load(f)
    print('Swear check channels loaded successfully.')
  except :
    print('Swear check channels loading process failed.')
  return

def save_swear_check_free_channels() :
  global swear_check_free_channels
  
  try :
    with open('swear_free_channels.bin', 'wb') as f :
      pickle.dump(swear_check_free_channels, f)
    print('Swear check channels saved successfully.')
  except :
    print('Swear check channels saving process failed.')
  return

@tasks.loop(seconds=10)
async def change_status():
  await client.change_presence(activity = discord.Game(next(status)))

async def chat_reviver_coroutine(fail_channel = None) :
  global bowing_server_guild_id, active_channel_id, words

  try :
    server = await client.fetch_guild(bowing_server_guild_id)
    active_channel = await server.fetch_channel(active_channel_id)
    bowers_assemble_role = server.get_role(966978458045513758)
    await active_channel.send("Heyy bowers!!! Talk about this word!! -: {**" + random.choice(words) + "**}" + bowers_assemble_role.mention)
    print('sent')
  except :
    print('Chat reviver failed.')
    if fail_channel != None :
      await fail_channel.send('* bows to tell you that the function failed, please try again! *')
  pass




async def tasks_loop() :
    global bowing_server_guild_id, active_channel_id, words
    # DO STUFF HERE, ONCE READY, THEN UNCOMMENT THE SECOND LINE OF ON_READY FUNC
    # https://stackoverflow.com/questions/64173987/how-to-make-the-bot-run-a-defined-function-at-a-specific-time-everyday-in-discor
    
    await client.wait_until_ready()
    
    while not client.is_closed():
        await chat_reviver_coroutine()
        await asyncio.sleep(3600)
    return

@client.event
async def on_ready():
    load_words()
    load_swear_check_free_channels()
    print('We have logged in as {0.user}'.format(client))
    client.loop.create_task(tasks_loop())
    change_status.start()
    
    game = discord.Game("Bowing the hell out of whoever calls me to their server and bawn bowing...")
    await client.change_presence(activity = game)

    try :
      bot_owner = client.get_user(bot_owner_id)
      if bot_owner.dm_channel == None :
          await bot_owner.create_dm()
      await bot_owner.dm_channel.send('Bowbot has successfully been started.')
    except :
      print('Ready action notif couldn\'t be sent to bowbot owner.')
    return

@client.event
async def on_member_join(member) :
    try :
        if member.dm_channel == None :
            await member.create_dm()
        await member.dm_channel.send('* bows to welcome you *')
        await member.guild.system_channel.send('* bows to welcome ' + member.name + ' *')
    except Exception as err :
        print('Some error occured in the on_member_join function', Exception, err)
        traceback.print_exc()
    return

@client.event
async def on_raw_member_remove(member) :
    try :
        if member.dm_channel == None :
            await member.create_dm()
        await member.dm_channel.send('* bows to say bye bye *')
        await member.guild.system_channel.send('* bows to say bye bye to ' + member.name + ' *')
    except Exception as err :
        print('Some error occured in the on_member_remove function', Exception, err)
        traceback.print_exc()
    return

# Define a simple View that gives us a confirmation menu
class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Confirming', ephemeral=True)
        self.value = True
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Cancelling', ephemeral=True)
        self.value = False
        self.stop()


@client.event
async def on_message(message):
    global bowing_server_guild_id, active_channel_id, swear_check_free_channels, swear_words, bot_owner_id
    try :
        if message.author == client.user :
            return
        print(message.author)
        print(message.content)
        if message.guild != None :
            print(message.guild.name)
            print(message.guild.owner.name)
            print(message.author == message.guild.owner)
            if message.guild.id == bowing_server_guild_id :
              active_channel_id = message.channel.id
            swear_words_in_msg = [word for word in message.content.split() if word.lower() in swear_words]
            if len(swear_words_in_msg) != 0 and message.channel.id not in swear_check_free_channels and message.author.id != bot_owner_id :
              await message.reply('* bows to' + message.author.mention + 'to tell them that their message has been deleted, since it contained inappropriate words. *')
              await message.delete()
        if message.content.lower() == '$$bow' :
            await message.channel.send('* bows cuz u gave me the command *')
        if message.content.lower() == '$$ping' :
            await message.channel.send('Bot has been successfully pinged! tyy <33~')
        if message.content.lower() == '$$test' :
          view = Confirm()
          await message.channel.send('Do you want to continue?', view = view)
          # Wait for the View to stop listening for input...
          await view.wait()
          if view.value is None:
              print('Timed out...')
          elif view.value:
              print('Confirmed...')
          else:
              print('Cancelled...')
        if message.content.lower() == '$$getrandomenglishword' :
          await chat_reviver_coroutine(message.channel)
    #     if message.content.lower() == '$$test' :
    #       await ui.components.send(message.channel, "Hello World", components=[
    # Button("press me", "my_custom_id", "green"),
    # Button("or press me!", "my_other_custom_id", emoji="😁", new_line=True)])
        if message.content.lower().startswith('$$bowbotswearcheck toggle off') :
          if len(message.channel_mentions) > 0 :
            swear_check_free_channels += [k.id for k in message.channel_mentions].copy()
            save_swear_check_free_channels()
            await message.channel.send('* bows to tell you that the mentioned channels are now exempted from bowbot\'s swear check *')
          else :
            swear_check_free_channels.append(message.channel.id)
            save_swear_check_free_channels()
            await message.channel.send('* bows to tell you that' + message.channel.mention + ' is now exempted from bowbot\'s swear check *')
        if message.content.lower() == '$$emobow' :
            await message.channel.send('http://static.skaip.org/img/emoticons/180x180/f6fcff/bow.gif')
        if message.content.lower() == '$$bowbotwebsite' :
            await message.channel.send('* bows to tell you that the official website of bowbot is -: https://bowbotwebsite.typedecker.repl.co/ *')
        if message.content.lower() == '$$bowbotdocs' or message.content.lower() == '$$bowbothelp' :
            await message.channel.send('* bows to tell you that you can find the docs here -: https://bowbotwebsite.typedecker.repl.co/docs.html *')
        if message.content.lower().startswith('$$bowforme ') :
            if len(message.mentions) != 0 :
                clean_message = message.clean_content[len('$$bowforme ') : ]
                for mention in message.mentions :
                    clean_message = clean_message.replace('@' + mention.name, '').replace(mention.mention, '')
                    print(mention.mention, mention.name, message.content, clean_message, clean_message.replace(mention.mention, ''))
                await message.channel.send('* ' + message.author.name + ' bows to ' + ' ,  '.join([k.mention for k in message.mentions]) + ' ' + clean_message + ' *')
            else :
                await message.channel.send('* ' + message.author.name + ' bows ' + message.content[len('$$bowforme ') : ] + ' *')
        if message.content.startswith('$$bowbot promote ') and message.author == message.guild.owner :
            target = message.mentions[0]
            promote_role = message.role_mentions[0]
            target_roles = [] + target.roles.copy()
            if not target_roles.__contains__(promote_role) :
                await message.mentions[0].add_roles(promote_role)
                await message.channel.send('Congratulations ' + target.name + '! You have been promoted to ' + promote_role.name)
                if target.dm_channel == None :
                    await target.create_dm()
                await target.dm_channel.send('Congratulations ' + target.name + '! You have been promoted to ' + promote_role.name)
            else :
                await message.channel.send('The member already has that role.')
        if message.content.startswith('$$bowbot demote ') and message.author == message.guild.owner :
            target = message.mentions[0]
            demote_role = message.role_mentions[0]
            target_roles = [] + target.roles.copy()
            if target_roles.__contains__(demote_role) :
                await message.mentions[0].remove_roles(demote_role)
                await message.channel.send('So unfortunate ' + target.name + '! You have been demoted from ' + demote_role.name)
                if target.dm_channel == None :
                    await target.create_dm()
                await target.dm_channel.send('So unfortunate ' + target.name + '! You have been demoted from ' + demote_role.name)
            else :
                await message.channel.send('The member already does not have that role.')
    except Exception as err :
        print('Some error occured in the message checker function', Exception, err)
        traceback.print_exc()
    return