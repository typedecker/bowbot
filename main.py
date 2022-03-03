import discord, os

client = discord.Client(fetch_offline_members = True)

# welcome_channels = {}

# def load_welcome_channels() :
#     global welcome_channels
    
#     try :
#         with open('welcome_channels_data.txt', 'r') as f :
#             welcome_channel_data = f.read()
#             welcome_channels = {k.split('###')[0] : k.split('###')[1] for k in welcome_channel_data.split('\n')}
#     except :
#         welcome_channels = {}
#     return

# def save_welcome_channel_data() :
#     global welcome_channels
    
#     try :
#         with open('welcome_channels_data.txt', 'w') as f :
#             f.write('\n'.join([k + '###' + welcome_channels[k] for k in welcome_channels]))
#         return True
#     except :
#         print('LOL SAVING WELCOME CHANNEL DATA FAILED * bows to say sorry *.')
#         return False

# def update_welcome_channel(server_name, channel_name) :
#     global welcome_channels
    
#     welcome_channels[server_name] = channel_name
#     return save_welcome_channel_data()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    
    game = discord.Game("Bowing the hell out of whoever calls me to their server and bawn bowing...")
    await client.change_presence(activity = game)
    return

@client.event
async def on_member_join(member) :
    if member.dm_channel == None :
        await member.create_dm()
    await member.dm_channel.send('* bows to welcome you *')
    await member.guild.system_channel.send('* bows to welcome ' + member.name + ' *')
    return

@client.event
async def on_message(message):
    print(message.author)
    print(message.content)
    print(message.guild.name)
    print(message.guild.owner.name)
    print(message.author == message.guild.owner)
    if message.author == client.user :
        return
    if message.content.lower() == '$$bow' :
        await message.channel.send('* bows cuz u gave me the command *')
    if message.content.lower().startswith('$$bowforme ') :
        if len(message.mentions) != 0 :
            clean_message = message.clean_content[len('$$bowforme ') : ]
            for mention in message.mentions :
                clean_message = clean_message.replace('@' + mention.name, '').replace(mention.mention, '')
                print(mention.mention, mention.name, message.content, clean_message, clean_message.content.replace(mention.mention, ''))
            await message.channel.send('* ' + message.author.name + ' bows to ' + ' ,  '.join([k.mention for k in message.mentions]) + ' ' + clean_message + ' *')
        else :
            await message.channel.send('* ' + message.author.name + ' bows ' + message.content[len('$$bowforme ') : ] + ' *')
    if message.content.startswith('$$bowbot promote ') and message.author == message.guild.owner :
        print('REACHED HERE LOL')
        content = message.content
        target = message.mentions[0]
        promote_role = message.role_mentions[0]
        target_roles = [] + target.roles.copy()
        print('HERE TOO LOL', promote_role.name, target.name)
        if not target_roles.__contains__(promote_role) :
            await message.mentions[0].add_roles(promote_role)
            await message.channel.send('Congratulations ' + target.name + '! You have been promoted to ' + promote_role.name)
            if target.dm_channel == None :
                await target.create_dm()
            await target.dm_channel.send('Congratulations ' + target.name + '! You have been promoted to ' + promote_role.name)
        else :
            await message.channel.send('The member already has that role.')
    if message.content.startswith('$$bowbot demote ') and message.author == message.guild.owner :
        content = message.content
        target = message.mentions[0]
        # role_name = content[content.index('[') + 1 : content.index(']')]
        demote_role = message.role_mentions[0]
        # demote_role = None
        # for role in message.guild.roles :
        #     if role.name == role_name :
        #         demote_role = role
        #         break
        target_roles = [] + target.roles.copy()
        if target_roles.__contains__(demote_role) :
            # target_roles.remove(demote_role)
            # message.mentions[0].edit(role = target_roles)
            await message.mentions[0].remove_roles(demote_role)
            await message.channel.send('So unfortunate ' + target.name + '! You have been demoted from ' + demote_role.name)
            if target.dm_channel == None :
                await target.create_dm()
            await target.dm_channel.send('So unfortunate ' + target.name + '! You have been demoted from ' + demote_role.name)
        else :
            await message.channel.send('The member already does not have that role.')

client.run(os.environ['BOT_TOKEN'])
