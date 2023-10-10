import discord
from discord.ext import commands
import random

class Fun(commands.Cog):
    """be help Fun"""

    def __init__(self, client):
        self.client = client

    @commands.command(name="kill", brief="Kill Someone", description="This command kills a user virtually.", usage="<user>", aliases=['die'])
    async def kill(self, ctx, member: discord.Member = None):
        dead_lines = [
        'jumped from an aeroplane',
        'You are dead',
        'your pc burst on your face while you were using discord',
        'Your teacher found you were sleeping in online class.. RIP',
        'A crocodile slaughtered you while you were swimming in a pond',
        'You thought you had a knife before you approached a thug.. ends up you didnt.. He shot you dead in the head.'
        ]
        death_response = random.choice(dead_lines)
        if(member == None):
            await ctx.send(ctx.author.mention+" "+death_response)
        else:
            await ctx.send(str(member)+" "+death_response)

    #bot
    @commands.command(name="intro", brief="About Bot", description="Gives an info about the bot")
    async def intro(self, ctx):
        await ctx.send("Hi! I am BE Bot, pronounced as BeYee Bot.")

    # @commands.command(name="spam", brief="Spam Messages", description="This command can be used by users with manage messages permissions to spam 10 messages to server")
    # @commands.has_permissions(manage_messages=True)
    # async def spam(self, ctx):
    #     i=0
    #     await ctx.send(ctx.author.mention+" requested to spam 10 messages")
    #     while(i<10):
    #         await ctx.send("Spamming as requested by user")
    #         i=i+1

    @commands.command(name="spawn", brief="Spawn something", description="The bot spawns something random when this command is used.")
    async def spawn(self, ctx):
        spawn_lines = [
            'just spawned a freaking mushroom',
            'tried to spawn a donkey but ended up spawning a dragon and died',
            'just spawned free money but a cow ate them all', 
            'Hey! stop spawning random items',
            'just spawned a dog with nine legs'
        ]

        spawn_response = random.choice(spawn_lines)
        await ctx.send(ctx.author.mention+" "+spawn_response)

    @commands.command(name="yeet", brief="Kill Someone", description="This command kills a user virtually.", usage="<user>", aliases=['yeeet', 'yeeeet', 'yeeeeet'])
    async def yeet(self, ctx, member: discord.Member = None):
        yeet_choice = random.randint(1, 6)
        if(yeet_choice == 1):
            death_response = 'was yeeeeeeted to Alaska'
        elif(yeet_choice == 2):
            death_response = 'was yeeeeeeted to China. We didnt find them. (*Maybe missing?*)'
        elif(yeet_choice == 3):
            death_response = 'was yeeeeeeted to Korea. *Now they can\'t come back*'
        elif(yeet_choice == 4):
            death_response = 'was yeeeeeeted to space.. *They were not in a space suit*'
        elif(yeet_choice == 5):
            death_response = 'was yeeeeeeted to heaven.. or maybe hell. *One way to find out*'
        elif(yeet_choice == 6):
            death_response = 'was yeeeeeeted from an aeroplane ||*The plane crashed a building later*||'
        if(member == None):
            await ctx.send(ctx.author.mention+" "+death_response)
        else:
            await ctx.send(str(member)+" "+death_response)


    



def setup(client):
    client.add_cog(Fun(client))