import discord, os

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    client.loop.create_task(tasks_loop())
    
    game = discord.Game("CWL for TYPE CREW in Clash Of Clans..Hehe ;)")
    await client.change_presence(activity = game)
    return

@client.event
async def on_message(message):
    if message.author == client.user :
        return
    if message.content.lower() == '$$bow' :
        await message.channel.send('* bows cuz u gave me the command *')

client.run(os.environ['BOT_TOKEN'])
