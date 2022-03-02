import discord, os

@client.event
async def on_message(message):
    if message.author == client.user :
        return
    if message.content.lower() == '$$bow' :
        await message.channel.send('* bows cuz u gave me the command *')

client.run(os.environ['BOT_TOKEN'])
