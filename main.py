import bot_rewrite
import os
import discord

while __name__ == '__main__':
    try:
        bot_rewrite.client.run(os.environ['BOT_TOKEN'])
    except discord.errors.HTTPException as e:
        print(e)
        print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
        os.system('kill 1')
    except Exception as e :
        print(e)
        print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
        os.system('kill 1')
