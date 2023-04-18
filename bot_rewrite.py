# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 13:49:34 2023

@author: DELL
"""

###---
import nest_asyncio
nest_asyncio.apply()
###---

#IMPORTS
import discord, os, traceback, asyncio, random, pickle, copy # General modules for discord bots
from typing import Optional, Literal, Union # Used to support slash command API
from discord.ext import tasks, commands # Used to support slash command API
# from flask import Flask # Used to run a webpage along with the bot, to keep the bot online on repl.it
from threading import Thread # Used to run a thread to run the bot on(using flask)
from itertools import cycle # Used to switch status to keep the bot alive
from discord import app_commands # To enable slash commands and their API
from command_management import CommandManager # For managing commands
from storage_management import GlobalDatabase, PermanentDatabase # For managing storage using discord categories
###---


# GLOBALS
bowing_server_guild_id = 948183518511509545
active_channel_id = 948183518511509548
bot_owner_id = 568446269610000385
words, swear_words = [], []
swear_check_free_channels = [] # ids
###---


### CLIENT CLASS DEFINITION
class BowbotClient(discord.Client):
    
    ### GENERAL SETUP
    def __init__(self):
        # Using self.intents gives an attribute error for some reason.
        intents = discord.Intents(guilds = True, dm_messages = True, members = True, messages = True, guild_messages = True, invites = True, message_content = True)
        super().__init__(chunk_guilds_at_startup = True, intents = intents)
        
        self.tree = app_commands.CommandTree(self) # for slash commands
        self.cust_status = cycle(['Bowing the hell out of whoever calls me to their server and bawn bowing...','Bowing the hell out of whoever calls me to their server and bawn bowing....'])
        
        self.command_manager = CommandManager(client = self)
        self.prefix = '$$' # other than the universal prefix(slash '/')
        
        self.settings_message_id = {}
        self.GI_BOT_DEFAULTS = {
            'server_swearcheck' : 'False',
            'welcome_messages' : 'True',
            'welcome_channel' : 'system',
            'welcome_dms' : 'True',
            'byebye_messages' : 'True',
            'byebye_channel' : 'system',
            'byebye_dms' : 'True',
            'revive_chat?' : 'True',
            'chat_revive_role' : 'None',
            'chat_revive_channel' : 'active{}',
            'server_language' : 'english',
            'global_chat_channel' : 'None',
            }
        
        # Global Database is intialized inside on_ready function instead, since it
        # requires access to the bot's info.
        return
    
    def load_words(self) :
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
    
    def load_swear_check_free_channels(self) :
          global swear_check_free_channels
        
          try :
            with open('swear_free_channels.bin', 'rb') as f :
              swear_check_free_channels = pickle.load(f)
            print('Swear check channels loaded successfully.')
          except :
            print('Swear check channels loading process failed.')
          return
    
    def save_swear_check_free_channels(self) :
          global swear_check_free_channels
          
          try :
            with open('swear_free_channels.bin', 'wb') as f :
              pickle.dump(swear_check_free_channels, f)
            print('Swear check channels saved successfully.')
          except :
            print('Swear check channels saving process failed.')
          return
    
    def update_swear_check_free_channels(self, channel) :
        global swear_check_free_channels
        swear_check_free_channels.append(channel.id)
        return
    
    def concat_swear_check_free_channels(self, channels) :
        global swear_check_free_channels
        swear_check_free_channels += [channel.id for channel in channels]
        return
    
    @tasks.loop(seconds = 10)
    async def change_status(self):
        await self.change_presence(activity = discord.Game(next(self.cust_status)))
    
    async def chat_reviver_coroutine(self, fail_channel = None) :
        global bowing_server_guild_id, active_channel_id, words
        # try :
        for server in self.guilds :
            print(server.name)
            local_db = await self.get_local_db(server)
            branch = await local_db.get_branch('general_info')
            server_info = (await branch.fetch_all())[0]['row_data']
            if server_info['revive_chat?'] != 'True' :
                continue
            sample = server_info['chat_revive_channel']
            revive_channel_info = sample[sample.index('{') + 1 : sample.index('}')]
            if revive_channel_info == '' :
                chat_revive_channel = (await server.fetch_channels())[0]
            else :
                chat_revive_channel = await server.fetch_channel(int(revive_channel_info))
            if server_info['chat_revive_role'] == 'None' :
                await chat_revive_channel.send("Heyy bowers!!! Talk about this word!! -: {**" + random.choice(words) + "**}")
            else :
                chat_revive_role = server.get_role(int(server_info['chat_revive_role']))
                await chat_revive_channel.send("Heyy bowers!!! Talk about this word!! -: {**" + random.choice(words) + "**}" + chat_revive_role.mention)
            print('SERVER', server)
            print('sent' + server.name)
            # server = await self.fetch_guild(bowing_server_guild_id)
            # active_channel = await server.fetch_channel(active_channel_id)
            # await active_channel.send("Heyy bowers!!! Talk about this word!! -: {**" + random.choice(words) + "**}" + chat_revive_role.mention)
        # except Exception as e :
        #   print('Chat reviver failed.[{0}]'.format(e))
        #   if fail_channel != None :
        #     await fail_channel.send('* bows to tell you that the function failed, please try again! *')
        pass
    
    async def tasks_loop(self) :
        global bowing_server_guild_id, active_channel_id, words
        # DO STUFF HERE, ONCE READY, THEN UNCOMMENT THE SECOND LINE OF ON_READY FUNC
        # https://stackoverflow.com/questions/64173987/how-to-make-the-bot-run-a-defined-function-at-a-specific-time-everyday-in-discor
        
        await self.wait_until_ready()
        
        while not self.is_closed():
            await self.chat_reviver_coroutine()
            await asyncio.sleep(3600)
        return
    
    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        await self.tree.sync()
    ###---
    
    ### CLIENT ON_READY FUNCTION
    async def on_ready(self):
        self.load_words()
        self.load_swear_check_free_channels()
        print('We have logged in as {0.user}'.format(self))
        print([guild.name for guild in self.guilds])
        self.loop.create_task(self.tasks_loop())
        self.change_status.start()
        
        game = discord.Game("Bowing the hell out of whoever calls me to their server and bawn bowing...")
        await self.change_presence(activity = game)
    
        try :
          bot_owner = self.get_user(bot_owner_id)
          if bot_owner.dm_channel == None :
              await bot_owner.create_dm()
          await bot_owner.dm_channel.send('Bowbot has successfully been started.')
        except :
          print('Ready action notif couldn\'t be sent to bowbot owner.')
        
        # Initializing database objects
        self.global_db = GlobalDatabase(self)
        self.global_db.print_info()
        return
    ###---
    
    async def on_member_join(self, member) :
        try :
            local_db = await self.get_local_db(member.guild)
            branch = await local_db.get_branch('general_info')
            info = (await branch.fetch_all())[0]['row_data']
            if info['welcome_dms'] == 'True' :
                if member.dm_channel == None :
                    await member.create_dm()
                await member.dm_channel.send('* bows to welcome you *')
            if info['welcome_messages'] == 'True' :
                if info['welcome_channel'] == 'first' :
                    welcome_channel = member.guild.channels[0]
                elif info['welcome_channel'] == 'system' :
                    welcome_channel = member.guild.system_channel
                else :
                    welcome_channel = member.guild.get_channel(int(info['welcome_channel']))
                await welcome_channel.send('* bows to welcome ' + member.name + ' *')
        except Exception as err :
            print('Some error occured in the on_member_join function', Exception, err)
            traceback.print_exc()
        return
    
    async def on_raw_member_remove(self, event) :
        member = event.member
        try :
            local_db = await self.get_local_db(member.guild)
            branch = await local_db.get_branch('general_info')
            info = (await branch.fetch_all())[0]['row_data']
            if info['byebye_dms'] == 'True' :
                if member.dm_channel == None :
                    await member.create_dm()
                await member.dm_channel.send('* bows to say bye bye *')
            if info['byebye_messages'] == 'True' :
                if info['byebye_channel'] == 'first' :
                    byebye_channel = member.guild.channels[0]
                elif info['byebye_channel'] == 'system' :
                    byebye_channel = member.guild.system_channel
                else :
                    byebye_channel = member.guild.get_channel(int(info['byebye_channel']))
                await byebye_channel.send('* bows to say bye bye to ' + member.name + ' *')
        except Exception as err :
            print('Some error occured in the on_member_join function', Exception, err)
            traceback.print_exc()
        # try :
        #     if member.dm_channel == None :
        #         await member.create_dm()
        #     await member.dm_channel.send('* bows to say bye bye *')
        #     await member.guild.system_channel.send('* bows to say bye bye to ' + member.name + ' *')
        # except Exception as err :
        #     print('Some error occured in the on_member_remove function', Exception, err)
        #     traceback.print_exc()
        return
    
    def print_message_debug_info(self, message) :
        print(message.author)
        print(message.content)
        if message.guild != None :
            print(message.guild.name)
            print(message.guild.owner.name)
            print(message.author == message.guild.owner)
        return
    
    async def check_and_delete_bad_words(self, message) :
        global active_channel_id
        if message.guild != None :
            if message.guild.id == bowing_server_guild_id :
                active_channel_id = message.channel.id
            swear_words_in_msg = [word for word in message.content.split() if word.lower() in swear_words]
            if len(swear_words_in_msg) != 0 and message.channel.id not in swear_check_free_channels and message.author.id != bot_owner_id :
                await message.reply('* bows to' + message.author.mention + 'to tell them that their message has been deleted, since it contained inappropriate words. *')
                await message.delete()
        return
    
    async def on_message(self, message) :
        global bowing_server_guild_id, active_channel_id, swear_check_free_channels, swear_words, bot_owner_id
        
        try :
            if message.author == client.user :
                return
            local_db = await self.get_local_db(message.guild)
            branch = await local_db.get_branch('general_info')
            data = (await branch.fetch_all())[0]['row_data']
            self.print_message_debug_info(message)
            if data['server_swearcheck'] == 'True' :
                await self.check_and_delete_bad_words(message)
            if message.content.startswith(self.prefix) : await self.command_manager.execute_command_text(message)
            else :
                if not message.author.bot :
                    if data['revive_chat?'] == 'True' and data['chat_revive_channel'][ : 6] == 'active' :
                        await branch.modify(data, {'chat_revive_channel' : 'active{' + str(message.channel.id) + '}'})
                    pass
                pass
        except Exception as err :
            print('Some error occured in the message checker function', Exception, err)
            traceback.print_exc()
        return
    
    async def get_local_db(self, server) :
        if len([k for k in server.categories if k.name == 'BOWBOTDB']) == 0 :
            print('STARTED w/o category process')
            await server.create_category_channel('BOWBOTDB')
            try :
                local_db = PermanentDatabase(self, server.id)
                gi_branch = await local_db.create_branch('general_info')
                info = await gi_branch.store(self.GI_BOT_DEFAULTS)
                self.settings_message_id[server.name] = copy.deepcopy(info['message_id'])
            except Exception as e :
                print(traceback.format_exc())
                print('ERROR IN STORING AND BRANCHING EFJHRUGHT[{0}]'.format(e))
            print("FINISHED")
        elif len([k for k in server.categories if k.name == 'BOWBOTDB']) > 1 :
            print('STARTED too many categories process')
            for category in [k for k in server.categories if k.name == 'BOWBOTDB'] :
                await category.delete()
                print('SAKUJO!')
                continue
            local_db = await self.get_local_db(server)
            print("FINISHED")
        else :
            print('STARTED category already exists process')
            local_db = PermanentDatabase(self, server.id)
            if 'general_info' not in local_db.branch_names :
                print('No channels')
                try :
                    gi_branch = await local_db.create_branch('general_info')
                    await gi_branch.store(self.GI_BOT_DEFAULTS)
                except Exception as e :
                    print(traceback.format_exc(), e)
                return
            print("FINISHED")
        return local_db
    
    async def on_guild_join(self, guild) :
        # await guild.create_category_channel('BOWBOTDB')
        await self.get_local_db(guild)
        return
    
    pass

# app = Flask('')

# @app.route('/')
# def main():
#   return 'Bowbot is ready.'

# def run():
#   app.run(host = '0.0.0.0', port = 8000)
#   return

# def keep_alive():
#   server = Thread(target = run)
#   server.start()
#   return

client = BowbotClient()


### Slash command definitions ---
@client.tree.command(description = 'the classic bow command')
async def bow(interaction: discord.Interaction) :
    args = [interaction]
    await client.command_manager.bow(args)
    return

@client.tree.command()
async def ping(interaction: discord.Interaction) :
    args = [interaction]
    await client.command_manager.ping(args)
    return

@client.tree.command()
async def test(interaction: discord.Interaction) :
    args = [interaction]
    await client.command_manager.test(args)
    return

@client.tree.command()
async def displaysettings(interaction: discord.Interaction) :
    args = [interaction]
    await client.command_manager.displaysettings(args)
    return

# CHANGE IF THE KEYS OF CLIENT.GI_BOT_DEFAULTS IS CHANGED.
@client.tree.command()
async def settings(interaction: discord.Interaction, setting_name : Literal['server_swearcheck', 'welcome_messages', 'welcome_channel', 'welcome_dms', 'revive_chat?', 'chat_revive_role', 'chat_revive_channel', 'server_language', 'global_chat_channel'], new_value: str) :
    args = [interaction, setting_name, new_value]
    await client.command_manager.settings(args)
    return

@client.tree.command()
async def getchanneltopic(interaction: discord.Interaction, channel : Optional[discord.TextChannel]) :
    args = [interaction, channel]
    await client.command_manager.getchanneltopic(args)
    return

@client.tree.command()
async def add_note(interaction : discord.Interaction, title : str, content : str) :
    args = [interaction, title, content]
    await client.command_manager.add_note(args)
    return

@client.tree.command()
async def list_notes(interaction : discord.Interaction) :
    args = [interaction]
    await client.command_manager.list_notes(args)
    return

@client.tree.command()
async def delete_note(interaction: discord.Interaction, note_title : str) :
    args = [interaction, note_title]
    await client.command_manager.delete_note(args)
    return

@client.tree.command()
async def getrandomenglishword(interaction: discord.Interaction) :
    args = [interaction]
    await client.command_manager.getrandomenglishword(args)
    return

@client.tree.command()
@app_commands.describe(cmd_flag = 'the flag that follows the command(usually "toggle")', switch = 'choose to turn it either on or off')
async def bowbotswearcheck(interaction : discord.Interaction, cmd_flag : Literal['toggle'], switch : Literal['on', 'off'], channel : Optional[discord.TextChannel] = None) :
    args = [interaction, cmd_flag, switch, channel]
    await client.command_manager.bowbotswearcheck(args)
    return

@client.tree.command()
async def emobow(interaction: discord.Interaction) :
    args = [interaction]
    await client.command_manager.emobow(args)
    return

@client.tree.command()
async def bowbotwebsite(interaction: discord.Interaction) :
    args = [interaction]
    await client.command_manager.bowbotwebsite(args)
    return

@client.tree.command()
async def bowbothelp(interaction: discord.Interaction) :
    args = [interaction]
    await client.command_manager.bowbothelp(args)
    return

@client.tree.command()
async def bowbotdocs(interaction: discord.Interaction) :
    args = [interaction]
    await client.command_manager.bowbotdocs(args)
    return

@client.tree.command()
async def help(interaction: discord.Interaction) :
    args = [interaction]
    await client.command_manager.help(args)
    return

@client.tree.command()
async def bowforme(interaction: discord.Interaction, mention : Optional[discord.Member] = None, message : str = '') :
    args = [interaction, mention, message]
    await client.command_manager.bowforme(args)
    return

@client.tree.command()
async def bowbot(interaction: discord.Interaction, switch : Literal['promote', 'demote'], member : discord.Member, role : discord.Role) :
    args = [interaction, switch, member, role]
    await client.command_manager.bowbot(args)
    return

###---



