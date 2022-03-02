import discord, os

client = discord.Client()

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
    global welcome_channels
    
    if member.dm_channel == None :
        await member.create_dm()
    await member.dm_channel.send('* bows to welcome you *')
    await member.guild.system_channel.send('* bows to welcome ' + member.name + ' *')
    return

@client.event
async def on_message(message):
    if message.author == client.user :
        return
    if message.content.lower() == '$$bow ' :
        await message.channel.send('* bows cuz u gave me the command *')
    if message.content.lower().startswith('$$bowforme ') :
        if len(message.mentions) != 0 :
            await message.channel.send('* ' + message.author.name + ' bows to @' + ', @'.join(message.mentions) + ' ' + message.content[len('$$bowforme ') : ] + ' *')
        else :
            await message.channel.send('* ' + message.author.name + ' bows ' + message.content[len('$$bowforme ') : ] + ' *')

client.run(os.environ['BOT_TOKEN'])
