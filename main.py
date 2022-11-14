import os
import discord
from bot import SuperBot

TOKEN = os.environ.get('DISCORD_TOKEN')


bot = SuperBot("myFirstBot")

class AsyncIterator:
    def __init__(self, seq):
        self.iter = iter(seq)

    async def __aiter__(self):
        return self

    async def __anext__(self):
        try:    
            return next(self.iter)
        except StopIteration:
            raise StopAsyncIteration

class MyClient(discord.Client):
    async def on_ready(self):
        print("Logged in as")
        print(self.user.name)
        print(self.user.id)
        print("-------------")

    async def on_message(self, message):
        if message.author == self.user:
            return
        elif message.content.startswith('$'):
            response = bot.handle_message(message.content[1:],
                                        message.author)
            if not response:
                return
            elif response[0] == 1:
                print(response[1])
                async for user, msg in AsyncIterator(response[1]):
                    await user.send(msg)

                await message.channel.send(response[2])
                n_msg = bot.pass_turn()
                msg = await message.channel.send(n_msg[2])
                await msg.add_reaction("1\u20e3")
                await msg.add_reaction("2\u20e3")
                await msg.add_reaction("3\u20e3")
            elif response[0] == 2:
                msg = await message.channel.send(response[1])
            else:
                await message.channel.send(response)
    
    async def on_reaction_add(self, reaction, user):
        if reaction.message.author == self.user:
            if user != self.user:
                response = bot.handle_reaction(reaction,user)
                if not response:
                    return
                elif response[0] == 3:
                    await reaction.message.channel.send(response[1])
                    n_msg = bot.pass_turn()
                    msg = await reaction.message.channel.send(n_msg[2])
                    async for x in AsyncIterator(range(3)):
                        if n_msg[1][x] != (0, 0):
                            await msg.add_reaction("{0}\u20e3".format(x+1))
                elif response[0] == 2:
                    msg = await reaction.message.channel.send(response[1])

                else:
                    await reaction.message.channel.send(response)
    
    
intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(TOKEN)