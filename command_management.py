# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 13:56:38 2023

@author: DELL
"""

### IMPORTS ---
import discord
# import storage_management
from discord import Embed, Colour
# from storage_management import PermanentDatabase
#---

### THE COMMAND MANAGER CLASS ---
class CommandManager() :
    def __init__(self, client) :
        self.commands = {}
        self.client = client
        
        # REGISTERING COMMANDS ---
        self.register_command(self.bow)
        self.register_command(self.ping)
        self.register_command(self.test)
        self.register_command(self.displaysettings)
        self.register_command(self.settings)
        self.register_command(self.getchanneltopic)
        self.register_command(self.add_note)
        self.register_command(self.list_notes)
        self.register_command(self.delete_note)
        self.register_command(self.getrandomenglishword)
        self.register_command(self.help)
        self.register_command(self.bowbotdocs)
        self.register_command(self.bowbothelp)
        self.register_command(self.bowbotwebsite)
        self.register_command(self.emobow)
        self.register_command(self.bowforme)
        self.register_command(self.bowbotswearcheck)
        self.register_command(self.bowbot)
        #---
        return
    
    ### Utility functions ---
    def register_command(self, command_func, command_name = None) :
        command_name = command_func.__name__ or command_name
        self.commands[command_name] = command_func
        return
    
    async def execute_command_text(self, message) :
        command_name = message.content.split()[0][len(self.client.prefix) : ]
        if command_name in list(self.commands.keys()) :
            args = [message] + message.content.split(' ')[1 : ].copy()
            await self.commands[command_name](args)
            print('Found and executed the command [in a text based way.]' + '[{0}]'.format(command_name))
        elif len([k for k in self.commands if message.content.startswith(self.client.prefix + k + ' ')]) > 0 :
            command_name = [k for k in self.commands if message.content.startswith(self.client.prefix + k + ' ')][0]
            args = [message] + message.content[len(self.client.prefix + command_name + ' ') + 1 : ].split(' ').copy()
            await self.commands[command_name](args)
            print('Found and executed the command [in a text based way.]' + '[{0}]'.format(command_name))
        else :
            print('Couldn\'t find the command. [{command}]'.format(command = command_name))
        return
    
    async def check_if_admin(self, member) :
        # Any member above the bot's role will be considered an admin.
        return (not member.top_role.is_assignable())
    
    async def check_if_interaction(self, content) :
        return ('response' in dir(content))
    
    ###---
    
    ### Command function definitions ---
    async def bow(self, args) :
        msg_or_interaction = args[0]
        if await self.check_if_interaction(msg_or_interaction) :
            await msg_or_interaction.response.send_message('* bows cuz u gave me the command *')
        else :
            await msg_or_interaction.channel.send('* bows cuz u gave me the command *')
        return
    
    async def ping(self, args) :
        msg_or_interaction = args[0]
        if await self.check_if_interaction(msg_or_interaction) :
            await msg_or_interaction.response.send_message('Bot has been successfully pinged! tyy <33~')
        else :
            await msg_or_interaction.channel.send('Bot has been successfully pinged! tyy <33~')
        return
    
    async def test(self, args) :
        moi = args[0]
        if await self.check_if_interaction(moi) :
            test_embed = moi.response.send_message(Embed(title = 'title', type = 'rich', description = 'description', color = Colour.orange()))
            test_embed.set_footer(text = 'cool footer')
        else :
            test_embed = moi.channel.send(Embed(title = 'title', type = 'rich', description = 'description', color = Colour.orange()))
            test_embed.set_footer(text = 'cool footer')
        return
    
    async def displaysettings(self, args) :
        moi = args[0]
        local_db = await self.client.get_local_db(moi.guild)
        branch = await local_db.get_branch('general_info')
        settings = (await branch.fetch_all())[0]['row_data']
        display_info = {}
        for k in settings :
            if k.endswith('_role') :
                if settings[k] != 'None' :
                    display_info[k] = moi.guild.get_role(int(settings[k])).name
                    continue
            if k.endswith('_channel') :
                if settings[k] == 'first' :
                    display_info[k] = moi.guild.channels[0].name
                    continue
                elif settings[k] == 'system' :
                    display_info[k] = moi.guild.system_channel.name
                    continue
                elif settings[k].startswith('active') :
                    display_info[k] = 'active'
                    continue
                elif settings[k] != 'None' and (not settings[k].startswith('active')) :
                    display_info[k] = moi.guild.get_channel(int(settings[k])).name
                    continue
            display_info[k] = settings[k]
            continue
        settings_embed = Embed(title = ('Bowbot Settings for ' + moi.guild.name), description = '* bows to tell you that given below is the bowbot\'s configuration for this server *', color = Colour.blue())
        for k in settings :
            settings_embed.add_field(name = k, value = display_info[k], inline = False)
            continue
        if await self.check_if_interaction(moi) :
            await moi.response.send_message('* bows to display the current configuration and settings of bowbot for this server *', embed = settings_embed)
        else :
            await moi.channel.send('* bows to display the current configuration and settings of bowbot for this server *', embed = settings_embed)
        return
    
    async def settings(self, args) :
        # register it to both slash and prefix command index.
        moi = args[0]
        setting = args[1]
        local_db = await self.client.get_local_db(moi.guild)
        branch = await local_db.get_branch('general_info')
        search_values = (await branch.fetch_all())[0]['row_data']
        if setting == 'welcome_channel' :
            if args[2] == 'first' :
                channel = (await moi.guild.fetch_channels())[0]
            elif args[2] == 'system' :
                channel = moi.guild.system_channel
            else :
                channel = [ch for ch in (await moi.guild.fetch_channels()) if ch.name == args[2]][0]
            await branch.modify(search_values, {setting : str(channel.id)})
        elif setting == 'chat_revive_role' :
            if args[2] == 'None' :
                val = 'None'
            else :
                chat_revive_role = [role for role in (await moi.guild.fetch_roles()) if role.name == args[2]][0]
                val = str(chat_revive_role.id)
            await branch.modify(search_values, {setting : val})
        elif setting == 'chat_revive_channel' :
            if args[2] == 'active' :
                val = 'active{ ' + str(moi.channel.id) + ' }'
            else :
                val = '{' + str([ch for ch in (await moi.guild.fetch_channels()) if ch.name == args[2]][0].id) + '}'
            await branch.modify(search_values, {setting : val})
            pass # ... code tmrw
        elif setting == 'global_chat_channel' :
            channel = [ch for ch in (await moi.guild.fetch_channels()) if ch.name == args[2]][0]
            await branch.modify(search_values, {setting : channel.id})
            pass # ... code tmrw
        else :
            await branch.modify(search_values, {setting : args[2]})
        
        if (await self.check_if_interaction(moi)) :
            await moi.response.send_message('* bows to tell you that the setting[{0}] has been successfully changed to the new value! *'.format(setting))
        else :
            await moi.channel.send('* bows to tell you that the setting[{0}] has been successfully changed to the new value! *'.format(setting))
        return
            
    
    async def getchanneltopic(self, args) :
        moi = args[0]
        if await self.check_if_interaction(moi) :
            channel = args[1] or moi.channel
            await moi.response.send_message('* bows to tell you that the topic of the channel is -: "{topic}" *'.format(topic = channel.topic))
        else :
            if len(args) > 1 :
                channel = args[1]
            else :
                channel = moi.channel
            await moi.channel.send('* bows to tell you that the topic of the channel is -: "{topic}" *'.format(topic = channel.topic))
        return
    
    async def add_note(self, args) :
        moi = args[0]
        if await self.check_if_interaction(moi) :
            user = moi.user
            note_title = args[1]
            note_content = args[2]
            # if not 'notes' in self.client.global_db.branch_names :
            #     notes_branch = await self.client.global_db.create_branch('notes')
            # else :
            #     notes_branch = self.client.global_db.get_branch('notes')
            notes_branch = await self.client.global_db.get_branch('notes')
            if len(await notes_branch.fetch_results({'user_id' : str(user.id), 'note_title' : note_title})) > 0 :
                await moi.response.send_message('* bows to tell you that a note with that title already exists. *')
                return
            await notes_branch.store({'user_id' : str(user.id), 'note_title' : note_title, 'note_content' : note_content})
            # await notes_branch.store(moi.user.id, args[2])
            await moi.response.send_message('* bows to tell you that your note has been stored. *')
        else :
            user = moi.author
            note_title = args[1]
            note_content = args[2]
            # if not 'notes' in self.client.global_db.branch_names :
            #     notes_branch = await self.client.global_db.create_branch('notes')
            # else :
            #     notes_branch = self.client.global_db.get_branch('notes')
            notes_branch = await self.client.global_db.get_branch('notes')
            if len(await notes_branch.fetch_results({'user_id' : str(user.id), 'note_title' : note_title})) > 0 :
                await moi.response.send_message('* bows to tell you that a note with that title already exists. *')
                return
            # await notes_branch.store(moi.author.id, args[2])
            await notes_branch.store({'user_id' : str(user.id), 'note_title' : note_title, 'note_content' : note_content})
            await moi.channel.send('* bows to tell you that your note has been stored. *')
        return
    
    async def list_notes(self, args) :
        moi = args[0]
        if await self.check_if_interaction(moi) :
            user = moi.user
            if 'notes' in self.client.global_db.branch_names :
                notes_branch = await self.client.global_db.get_branch('notes')
                user_notes = await notes_branch.fetch_results({'user_id' : str(user.id)})
                if len(user_notes) == 0 :
                    await moi.response.send_message('* bows to tell you that you have no notes saved to view! *')
                    return
                note_list_embed = Embed(title = (user.name + '\'s notes list'), description = '* bows to tell you that given below is a list of notes with a summary of the content inside it *', color = Colour.blue())
                for k in user_notes :
                    content_summary = k['row_data']['note_content']
                    if len(content_summary) > 1024 : content_summary = content_summary[ : 1024]
                    note_list_embed.add_field(name = k['row_data']['note_title'], value = content_summary, inline = False)
                    continue
                await moi.response.send_message('* bows to display the list of notes *', embed = note_list_embed)
            else :
                await moi.response.send_message('* bows to tell you that you have no notes saved to view! *')
        else :
            user = moi.author
            if 'notes' in self.client.global_db.branch_names :
                notes_branch = await self.client.global_db.get_branch('notes')
                user_notes = await notes_branch.fetch_results({'user_id' : str(user.id)})
                if len(user_notes) == 0 :
                    await moi.response.send_message('* bows to tell you that you have no notes saved to view! *')
                    return
                note_list_embed = Embed(title = (user.name + '\'s notes list'), description = '* bows to tell you that given below is a list of notes with a summary of the content inside it *', color = Colour.blue())
                for k in user_notes :
                    content_summary = k['row_data']['note_content']
                    if len(content_summary) > 1024 : content_summary = content_summary[ : 1024]
                    note_list_embed.add_field(name = k['row_data']['note_title'], value = content_summary, inline = False)
                    continue
                await moi.channel.send('* bows to display the list of notes *', embed = note_list_embed)
            else :
                await moi.channel.send('* bows to tell you that you have no notes saved to view! *')
        return
    
    async def delete_note(self, args) :
        moi = args[0]
        note_title = args[1]
        notes_branch = await self.client.global_db.get_branch('notes')
        if await self.check_if_interaction(moi) :
            user = moi.user
            user_notes = await notes_branch.fetch_results({'user_id' : str(user.id), 'note_title' : note_title})
            if len(user_notes) == 0 :
                await moi.response.send_message('* bows to tell you that there are no notes saved with the title {note_title}, to delete. *'.format(note_title = note_title))
                return
            try :
                await notes_branch.delete({'user_id' : str(user.id), 'note_title' : note_title})
                await moi.response.send_message('* bows to tell you that the note title {0} has been successfully deleted. *'.format(note_title))
            except Exception as e :
                await moi.response.send_message('* bows to tell you that some error occurred while trying to delete the note. *')
                print(e)
        else :
            user = moi.author
            user_notes = await notes_branch.fetch_results({'user_id' : str(user.id), 'note_title' : note_title})
            if len(user_notes) == 0 :
                await moi.channel.send('* bows to tell you that there are no notes saved with the title {note_title}, to delete. *'.format(note_title = note_title))
                return
            try :
                await notes_branch.delete({'user_id' : str(user.id), 'note_title' : note_title})
                await moi.channel.send('* bows to tell you that the note title {0} has been successfully deleted. *'.format(note_title))
            except Exception as e :
                await moi.channel.send('* bows to tell you that some error occurred while trying to delete the note. *')
                print(e)
        return
    
    async def getrandomenglishword(self, args) :
        msg_or_interaction = args[0]
        if await self.check_if_interaction(msg_or_interaction) : msg_or_interaction.response.send_message('* bows to inform that the message was sent! *')
        await self.client.chat_reviver_coroutine(msg_or_interaction.channel)
        return
    
    async def bowbotswearcheck(self, args) : # works like bowbotswearcheck toggle off for now. (CHANGE IT CUZ U FORGOT EARLIER)
        msg_or_interaction = args[0]
        if await self.check_if_interaction(msg_or_interaction) :
            if not await self.check_if_admin(msg_or_interaction.user) :
                await msg_or_interaction.response.send_message('* bows to tell you that this command can only be executed by a member bearing the server administrator permission. *')
            if args[3] != None :
                self.client.concat_swear_check_free_channels([args[3].id])
                self.client.save_swear_check_free_channels()
                await msg_or_interaction.response.send_message('* bows to tell you that the mentioned channels are now exempted from bowbot\'s swear check *')
            else :
                self.client.update_swear_check_free_channels(msg_or_interaction.channel)
                self.client.save_swear_check_free_channels()
                await msg_or_interaction.response.send_message('* bows to tell you that' + msg_or_interaction.channel.mention + ' is now exempted from bowbot\'s swear check *')
        else :
            if not await self.check_if_admin(msg_or_interaction.author) :
                await msg_or_interaction.channel.send('* bows to tell you that this command can only be executed by a member bearing the server administrator permission. *')
            if len(msg_or_interaction.channel_mentions) > 0 :
                self.client.concat_swear_check_free_channels([k.id for k in msg_or_interaction.channel_mentions].copy())
                self.client.save_swear_check_free_channels()
                await msg_or_interaction.channel.send('* bows to tell you that the mentioned channels are now exempted from bowbot\'s swear check *')
            else :
                self.client.update_swear_check_free_channels(msg_or_interaction.channel)
                self.client.save_swear_check_free_channels()
                await msg_or_interaction.channel.send('* bows to tell you that' + msg_or_interaction.channel.mention + ' is now exempted from bowbot\'s swear check *')
        return
    
    async def emobow(self, args) :
        moi = args[0]
        if await self.check_if_interaction(moi) :
            await moi.response.send_message('http://static.skaip.org/img/emoticons/180x180/f6fcff/bow.gif')
        else :
            await moi.channel.send('http://static.skaip.org/img/emoticons/180x180/f6fcff/bow.gif')
        return
    
    async def bowbotwebsite(self, args) :
        moi = args[0]
        if await self.check_if_interaction(moi) :
            await moi.response.send_message('* bows to tell you that the official website of bowbot is -: https://bowbotwebsite.typedecker.repl.co/ *')
        else :
            await moi.channel.send('* bows to tell you that the official website of bowbot is -: https://bowbotwebsite.typedecker.repl.co/ *')
        return
    
    async def bowbotdocs(self, args) :
        moi = args[0]
        if await self.check_if_interaction(moi) :
            await moi.response.send_message('* bows to tell you that you can find the docs here -: https://bowbotwebsite.typedecker.repl.co/docs.html *')
        else :
            await moi.channel.send('* bows to tell you that you can find the docs here -: https://bowbotwebsite.typedecker.repl.co/docs.html *')
        return
    
    async def help(self, args) :
        moi = args[0]
        if await self.check_if_interaction(moi) :
            await moi.response.send_message('* bows to tell you that you can find the docs here -: https://bowbotwebsite.typedecker.repl.co/docs.html *')
        else :
            await moi.channel.send('* bows to tell you that you can find the docs here -: https://bowbotwebsite.typedecker.repl.co/docs.html *')
        return
    
    async def bowbothelp(self, args) :
        moi = args[0]
        if await self.check_if_interaction(moi) :
            await moi.response.send_message('* bows to tell you that you can find the docs here -: https://bowbotwebsite.typedecker.repl.co/docs.html *')
        else :
            await moi.channel.send('* bows to tell you that you can find the docs here -: https://bowbotwebsite.typedecker.repl.co/docs.html *')
        return
    
    async def bowforme(self, args) :
        moi = args[0]
        if await self.check_if_interaction(moi) :
            mention = args[1]
            message = args[2]
            if mention != None :
                await moi.response.send_message('* {author} bows to {mentions} {message} *'.format(author = moi.user.name, mentions = mention.mention, message = message))
            else :
                await moi.response.send_message('* {author} bows {message} *'.format(author = moi.user.name, message = message))
        else :
            if len(moi.mentions) != 0 :
                clean_message = moi.clean_content[len('$$bowforme ') : ]
                for mention in moi.mentions :
                    clean_message = clean_message.replace('@' + mention.name, '').replace(mention.mention, '')
                    print(mention.mention, mention.name, moi.content, clean_message, clean_message.replace(mention.mention, ''))
                await moi.channel.send('* ' + moi.user.name + ' bows to ' + ' ,  '.join([k.mention for k in moi.mentions]) + ' ' + clean_message + ' *')
            else :
                await moi.channel.send('* ' + moi.user.name + ' bows ' + moi.content[len('$$bowforme ') : ] + ' *')
        return
    
    async def bowbot(self, args) :
        moi = args[0]
        if await self.check_if_interaction(moi) :
            switch = args[1]
            if switch == 'promote' and await self.check_if_admin(moi.user) :
                target = args[2]
                promote_role = args[3]
                target_roles = [] + target.roles.copy()
                if not target_roles.__contains__(promote_role) :
                    await target.add_roles(promote_role)
                    await moi.response.send_message('Congratulations ' + target.mention + '! You have been promoted to ' + promote_role.mention)
                    try :
                        if target.dm_channel == None :
                            await target.create_dm()
                        await target.dm_channel.send('Congratulations ' + target.mention + '! You have been promoted to ' + promote_role.mention)
                    except Exception as e :
                        print(e)
                else :
                    await moi.response.send_message('The member already has that role.')
            if switch == 'demote' and await self.check_if_admin(moi.user) :
                target = args[2]
                demote_role = args[3]
                target_roles = [] + target.roles.copy()
                if target_roles.__contains__(demote_role) :
                    await target.remove_roles(demote_role)
                    await moi.response.send_message('So unfortunate ' + target.mention + '! You have been demoted from ' + demote_role.mention)
                    try :
                        if target.dm_channel == None :
                            await target.create_dm()
                        await target.dm_channel.send('So unfortunate ' + target.mention + '! You have been demoted from ' + demote_role.mention)
                    except Exception as e :
                        print(e)
                else :
                    await moi.response.send_message('The member already does not have that role.')
        else :
            if moi.content.startswith('$$bowbot promote ') and await self.check_if_admin(moi.author) :
                target = moi.mentions[0]
                promote_role = moi.role_mentions[0]
                target_roles = [] + target.roles.copy()
                if not target_roles.__contains__(promote_role) :
                    await target.add_roles(promote_role)
                    await moi.channel.send('Congratulations ' + target.mention + '! You have been promoted to ' + promote_role.mention)
                    try :
                        if target.dm_channel == None :
                            await target.create_dm()
                        await target.dm_channel.send('Congratulations ' + target.mention + '! You have been promoted to ' + promote_role.mention)
                    except Exception as e :
                        print(e)
                else :
                    await moi.channel.send('The member already has that role.')
            if moi.content.startswith('$$bowbot demote ') and await self.check_if_admin(moi.author) :
                target = moi.mentions[0]
                demote_role = moi.role_mentions[0]
                target_roles = [] + target.roles.copy()
                if target_roles.__contains__(demote_role) :
                    await target.remove_roles(demote_role)
                    await moi.channel.send('So unfortunate ' + target.mention + '! You have been demoted from ' + demote_role.mention)
                    try :
                        if target.dm_channel == None :
                            await target.create_dm()
                        await target.dm_channel.send('So unfortunate ' + target.mention + '! You have been demoted from ' + demote_role.mention)
                    except Exception as e :
                        print(e)
                else :
                    await moi.channel.send('The member already does not have that role.')
        return
    ###---
    pass
###---

### Debug stuff ---
if __name__ == '__main__' :
    cm = CommandManager(2)
    print(cm.commands)
    cm.bow()
    print(cm.commands)
###---

##REMINDER -: DO THE INTERACTION.RESPONSE.SEND_MSG THING FOR ALL COMMANDS. DONE.