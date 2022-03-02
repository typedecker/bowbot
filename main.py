import discord, os

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    
    game = discord.Game("Bowing the hell out of whoever calls me to their server and bawn bowing...")
    await client.change_presence(activity = game)
    return

@client.event
async def on_message(message):
    if message.author == client.user :
        return
    if message.content.lower() == '$$bow' :
        await message.channel.send('* bows cuz u gave me the command *')

client.run(os.environ['BOT_TOKEN'])
