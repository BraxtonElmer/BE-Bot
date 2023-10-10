# Game Cog for BE Bot
# Author: BraxtonElmer

import discord
from discord.ext import commands
import random
import mysql.connector
import datetime
import asyncio
import config

class Games(commands.Cog):
    """be help Games"""

    def __init__(self, client):
        self.client = client


    @commands.command(name="rpsm", brief="Play Rock Paper Scissors Multiplayer with your friends!", description="Play Rock Paper Scissors with your friends! This game is very interactive and your choices will not be known to your opponent!")
    async def rpsm(self, ctx):

#################################################################################################################################
        

        players = []
        players_name = []
        players_username=[]
        players_mention=[]

        message = await ctx.send("Welcome to the game of **Multiplayer** Rock Paper Scissors!!\nReact to this message to enter the game (Only 2 players can play this game)\nTime Remaining: 10")
        await message.add_reaction('✅')
        secondint = 10
        while True:
            secondint -= 1
            if secondint == 0:
                await ctx.send("Timer Ended! No new Entries will be recorded anymore.")
                break
            await message.edit(content=f"Welcome to the game of **Multiplayer** Rock Paper Scissors!!\nReact to this message to enter the game (Only 2 players can play this game)\nTime Remaining: {secondint}")
            await asyncio.sleep(1)

        message = await ctx.fetch_message(message.id)

        for reaction in message.reactions:
            if reaction.emoji == '✅':
                async for user in reaction.users():
                    if user != self.client.user:
                        players.append(user.id)
                        players_username.append(user)
                        players_name.append(user.name)
                        players_mention.append(user.mention)

        if len(players) > 2:
            await ctx.send('More than 2 players reacted to the message.. Only 2 players can play the game.')
            return
        elif len(players) < 2:
            await ctx.send('2 players are required to play this game but less than 2 people reacted..')
            return
        else:
            # print("rpc multi game started.")
            if(str(players_name[0]) == (players_name[1])):
                players_list=players_username
            else:
                players_list=players_name




        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        await ctx.send(ctx.author.mention+" Nice! **Now type the winning score:** (The first person to reach this score will win.)")
        reply = await self.client.wait_for('message', check=check)
        if(reply.content.isnumeric()):
            games = int(reply.content)
            if games > 30:
                await ctx.send("You cannot play for a score more than 30! Why? you may ask, that is done to avoid mental depression out of rock paper scissors.")
                return
        else:
            await ctx.send(ctx.author.mention+" You did not enter a valid number.")
            return

        await ctx.send("Ok! A rock paper scissors game between **"+str(players_mention[0])+"** and **"+str(players_mention[1])+"** for **"+str(games)+"** points!\nLet the game Begin now! Enter your choices in DM!")

##########################################################################################################################

        dm_intro="Hi!\nYou have to type your choice here in DM.\nFor choosing rock, you can type `rock` or `r`.\nFor choosing paper type `paper` or `p`.\nFor choosing scissors, type `scissors` or `s`."

        user_1= ctx.guild.get_member(players[0])
        user_2= ctx.guild.get_member(players[1])

        await user_1.send(dm_intro+"\nEnter your choice now:")
        await user_2.send(dm_intro+"\nYou can send your choice after "+str(players_list[0])+" makes their choice..")
        d_c=1

    
#########################################################################################
        user_1_score = 0
        user_2_score = 0
        c = 0
        while(c < games):
            if(d_c==0):
                await asyncio.sleep(5)
                await ctx.send("Send your next choices in DM!")
                await user_1.send("Type your next choice here: ")
                await user_2.send("Get ready to type your next choice!")

            def check_1(m_1):
                return m_1.author == players_username[0] and m_1.guild is None
        
            def check_2(m_2):
                return m_2.author == players_username[1] and m_2.guild is None
            while(True):
                msg_1 = await self.client.wait_for('message', check=check_1)
                if (str(msg_1.content.lower()) == "r" or str(msg_1.content.lower()) == "rock" or str(msg_1.content.lower()) == "paper" or str(msg_1.content.lower()) == "p" or str(msg_1.content.lower()) == "scissors" or str(msg_1.content.lower()) == "s"):
                    await user_1.send(str(players_list[1])+" is still making their choice. After they make their choice results will be shown in "+ctx.channel.mention)
                    break
                else:
                    await user_1.send("Not a valid choice. Enter either `rock`, `paper`, `scissors` or `r`, `p`, `s`.")
                    
            await user_2.send(str(players_list[0])+" Have made their choice. Enter your choice now:")
            # msg_2 = await self.client.wait_for('message', check=check_2)
            while(True):
                msg_2 = await self.client.wait_for('message', check=check_2)
                if (str(msg_2.content.lower()) == "r" or str(msg_2.content.lower()) == "rock" or str(msg_2.content.lower()) == "paper" or str(msg_2.content.lower()) == "p" or str(msg_2.content.lower()) == "scissors" or str(msg_2.content.lower()) == "s"):
                    await user_2.send("Check the results in: "+ctx.channel.mention)
                    break
                else:
                    await user_2.send("Not a valid choice. Enter either `rock`, `paper`, `scissors` or `r`, `p`, `s`.")

            if(str(msg_1.content).lower() == "rock"or str(msg_1.content).lower()=="r"):
                user_1_choice_val = "rock"
            elif(str(msg_1.content).lower() == "paper" or str(msg_1.content).lower() == "p"):  
                user_1_choice_val ="paper"   
            elif(str(msg_1.content).lower() == "scissors" or str(msg_1.content).lower()=="s"):      
                user_1_choice_val ="scissors"

            if(str(msg_2.content).lower() == "rock"or str(msg_2.content).lower()=="r"):
                user_2_choice_val = "rock"
            elif(str(msg_2.content).lower() == "paper" or str(msg_2.content).lower() == "p"):  
                user_2_choice_val ="paper"   
            elif(str(msg_2.content).lower() == "scissors" or str(msg_2.content).lower()=="s"):      
                user_2_choice_val ="scissors"


            if(user_1_choice_val == "rock" and user_2_choice_val=="rock"):
                embed=discord.Embed(title="Same Choice", description=str(players_list[0])+" Chose rock\n"+str(players_list[1])+" Chose Rock", color=discord.Color.blue())

            elif(user_1_choice_val == "rock" and user_2_choice_val=="paper"):
                user_2_score = user_2_score + 1
                embed=discord.Embed(title=str(players_list[1])+" Gets a point!", description=str(players_list[0])+" Chose rock\n"+str(players_list[1])+" Chose paper", color=discord.Color.blue())

            elif(user_1_choice_val == "rock" and user_2_choice_val=="scissors"):
                user_1_score = user_1_score + 1
                embed=discord.Embed(title=str(players_list[0])+" Gets a point!", description=str(players_list[0])+" Chose rock\n"+str(players_list[1])+" Chose scissors", color=discord.Color.blue())

            elif(user_1_choice_val == "paper" and user_2_choice_val=="rock"):
                user_1_score = user_1_score + 1
                embed=discord.Embed(title=str(players_list[0])+" Gets a point!", description=str(players_list[0])+" Chose paper\n"+str(players_list[1])+" Chose rock", color=discord.Color.blue())

            elif(user_1_choice_val == "paper" and user_2_choice_val=="paper"):
                embed=discord.Embed(title="Same choice", description=str(players_list[0])+" Chose paper\n"+str(players_list[1])+" Chose paper", color=discord.Color.blue())

            elif(user_1_choice_val == "paper" and user_2_choice_val=="scissors"):
                user_2_score = user_2_score + 1
                embed=discord.Embed(title=str(players_list[1])+" Gets a point!", description=str(players_list[0])+" Chose paper\n"+str(players_list[1])+" Chose scissors", color=discord.Color.blue())

            elif(user_1_choice_val == "scissors" and user_2_choice_val=="rock"):
                user_2_score = user_2_score + 1
                embed=discord.Embed(title=str(players_list[1])+" Gets a point!", description=str(players_list[0])+" Chose scissors\n"+str(players_list[1])+" Chose rock", color=discord.Color.blue())

            elif(user_1_choice_val == "scissors" and user_2_choice_val=="paper"):
                user_1_score = user_1_score + 1
                embed=discord.Embed(title=str(players_list[0])+" Gets a point!", description=str(players_list[0])+" Chose scissors\n"+str(players_list[1])+" Chose paper", color=discord.Color.blue())

            elif(user_1_choice_val == "scissors" and user_2_choice_val=="scissors"):
                embed=discord.Embed(title="Same Choice", description=str(players_list[0])+" Chose scissors\n"+str(players_list[1])+" Chose scissors", color=discord.Color.blue())
           
            embed.add_field(name=str(players_list[0])+"'s score: "+str(user_1_score), value="** **", inline=True)
            embed.add_field(name=str(players_list[1])+"'s score: "+str(user_2_score), value="** **", inline=True)
            embed.set_footer(text="First to reach "+str(games)+" points wins.")
            await ctx.send(embed=embed)

            if user_1_score < user_2_score:
                c = user_2_score
            else:
                c = user_1_score

            d_c=0

        #while loop end

        if(user_1_score < user_2_score):
            await user_2.send("**You Win!** Congrats!")
            await user_1.send("You Lost. Better Luck next time.")
            await ctx.send("\n**"+str(players_list[1])+" wins!** Congrats "+players_mention[1]+"!")
        else:
            await user_1.send("**You Win!** Congrats!")
            await user_2.send("You Lost. Better Luck next time.")
            await ctx.send("\n**"+str(players_list[0])+" wins!** "+players_mention[0]+"Congrats!")




########################################## ROCK PAPER SCISSORS ##########################################

    @commands.command(name="rps", brief="Play Rock, Paper, Scissors and if you win you can get BE coins (Singleplayer)", description="You can bet an amount to play rock paper scissors with the bot! If you win, you will get the amount and if you lose, you lose the amount.")
    async def rps(self, ctx):
        await ctx.send(ctx.author.mention+" Welcome to the game of rock paper scissors! In this game, you will have to enter a bet amount which you will get if you win and lose if you lose..\nYou can enter `rock`, `paper`, `scissors` or also `r`, `p`, `s`! \n**Enter your bet amount:**")
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        reply = await self.client.wait_for('message', check=check)
        if(reply.content.isnumeric()):
            mydb = mysql.connector.connect(
        host=config.sql_host,
        user=config.sql_user,
        password=config.sql_pass,
        database=config.sql_db
            )
            mycursor = mydb.cursor()
            mycursor.execute("SELECT money FROM user_data WHERE user_id='"+str(ctx.author.id)+"'")
            user_rpc_get = mycursor.fetchall()
            for user_rpc_data in user_rpc_get:
                user_bal = user_rpc_data[0]
            bet_amt = int(reply.content)
            if bet_amt < 100:
                await ctx.send("Bet amount cannot be lower than 100 BE coins.")
                return
            if bet_amt > user_bal:
                await ctx.send("You do not have "+str(bet_amt)+" BE coins.")
                return
        else:
            await ctx.send(ctx.author.mention+" You did not enter a valid number.")
            return
        await ctx.send(ctx.author.mention+" Nice! You will be playing rock paper scissors with a bet amount of "+str(bet_amt)+" BE coins!\n(You can type `exit` to exit the game. **If you type `exit` to leave the game** and if you are in a losing score, you will lose the BE coins you bet and if you are in a winning score you will not get the BE coins you bet. This is done to prevent fraudulent activities.)\n**Now type the winning score:** (The first person to reach this score will win.)")
        reply = await self.client.wait_for('message', check=check)
        if(reply.content.isnumeric()):
            games = int(reply.content)
            if games > 30:
                await ctx.send("You cannot play fora score more than 30! Why? you may ask, that is done to avoid mental depression out of rock paper scissors.")
                return
        else:
            await ctx.send(ctx.author.mention+" You did not enter a valid number.")
            return
        await ctx.send(ctx.author.mention+" Good! First person to reach "+str(games)+" points wins "+str(bet_amt)+" BE coins!")
        secondint = 6
        message = await ctx.send("Game will start in: 5")
        while True:
            secondint -= 1
            if secondint == 0:
                await message.edit(content="Game will Start now!")
                break
            await message.edit(content=f"Game will start in: {secondint}")
            await asyncio.sleep(1)
        c = 0
        bot_score = 0
        user_score = 0
        while(c < games):

            await ctx.send("Enter your choice: (Rock, Paper or Scissors)")
            reply = await self.client.wait_for('message', check=check)
            if (str(reply.content) == "exit"):
                if(bot_score > user_score):
                    mydb = mysql.connector.connect(
                    host=config.sql_host,
                    user=config.sql_user,
                    password=config.sql_pass,
                    database=config.sql_db
                    )
                    mycursor = mydb.cursor()
                    mycursor.execute("SELECT money FROM user_data WHERE user_id='"+str(ctx.author.id)+"'")
                    user_rpc_get = mycursor.fetchall()
                    for user_rpc_data in user_rpc_get:
                        user_bal_kick = user_rpc_data[0]
                    new_bal_exit = user_bal_kick - bet_amt
                    update_exit_sql = "UPDATE `user_data` SET `money`="+str(new_bal_exit)+" WHERE user_id = '"+str(ctx.author.id)+"'"
                    mycursor.execute(update_exit_sql)
                    mydb.commit()
                    await ctx.send("Thanks for playing! The game has now ended.\n(You lost "+str(bet_amt)+" BE coins since you exited the game with a lower score.")
                    return
                else:
                    await ctx.send("Thanks for playing! The game has now ended.")
                return
            if(str(reply.content).lower() == "rock"or str(reply.content).lower()=="r"):
                user_choice_val = "rock"
            elif(str(reply.content).lower() == "paper" or str(reply.content).lower() == "p"):  
                user_choice_val ="paper"   
            elif(str(reply.content).lower() == "scissors" or str(reply.content).lower()=="s"):      
                user_choice_val ="scissors"
            else:
                user_choice_val = "none"


            bot_choice_number = random.randint(1,3)
            if(bot_choice_number == 1):
                bot_choice_val = "rock"
            elif(bot_choice_number == 2):
                bot_choice_val = "paper"
            else:
                bot_choice_val = "scissors"
            
            if(user_choice_val == "rock" and bot_choice_val=="rock"):
                embed=discord.Embed(title="Same Choice", description="Bot Chose Rock", color=discord.Color.blue())
                embed.add_field(name="Your Score: "+str(user_score), value="** **", inline=True)
                embed.add_field(name="Bot Score: "+str(bot_score), value="** **", inline=True)
                embed.set_footer(text="First to reach "+str(games)+" points wins "+str(bet_amt)+" BE coins.\nType `exit` to leave the game.")
                await ctx.send(embed=embed)
            elif(user_choice_val == "rock" and bot_choice_val=="paper"):
                bot_score = bot_score + 1
                embed=discord.Embed(title="Bot Gets a point.", description="Bot Chose paper", color=discord.Color.blue())
                embed.add_field(name="Your Score: "+str(user_score), value="** **", inline=True)
                embed.add_field(name="Bot Score: "+str(bot_score), value="** **", inline=True)
                embed.set_footer(text="First to reach "+str(games)+" points wins "+str(bet_amt)+" BE coins.\nType `exit` to leave the game.")
                await ctx.send(embed=embed)
            elif(user_choice_val == "rock" and bot_choice_val=="scissors"):
                user_score = user_score + 1
                embed=discord.Embed(title="You Get a point!", description="Bot Chose scissors", color=discord.Color.blue())
                embed.add_field(name="Your Score: "+str(user_score), value="** **", inline=True)
                embed.add_field(name="Bot Score: "+str(bot_score), value="** **", inline=True)
                embed.set_footer(text="First to reach "+str(games)+" points wins "+str(bet_amt)+" BE coins.\nType `exit` to leave the game.")
                await ctx.send(embed=embed)
            elif(user_choice_val == "paper" and bot_choice_val=="rock"):
                user_score = user_score + 1
                embed=discord.Embed(title="You Get a point!", description="Bot Chose rock", color=discord.Color.blue())
                embed.add_field(name="Your Score: "+str(user_score), value="** **", inline=True)
                embed.add_field(name="Bot Score: "+str(bot_score), value="** **", inline=True)
                embed.set_footer(text="First to reach "+str(games)+" points wins "+str(bet_amt)+" BE coins.\nType `exit` to leave the game.")
                await ctx.send(embed=embed)
            elif(user_choice_val == "paper" and bot_choice_val=="paper"):
                embed=discord.Embed(title="Same choice", description="Bot Chose paper", color=discord.Color.blue())
                embed.add_field(name="Your Score: "+str(user_score), value="** **", inline=True)
                embed.add_field(name="Bot Score: "+str(bot_score), value="** **", inline=True)
                embed.set_footer(text="First to reach "+str(games)+" points wins "+str(bet_amt)+" BE coins.\nType `exit` to leave the game.")
                await ctx.send(embed=embed)
            elif(user_choice_val == "paper" and bot_choice_val=="scissors"):
                bot_score = bot_score + 1
                embed=discord.Embed(title="Bot Gets a point", description="Bot Chose scissors", color=discord.Color.blue())
                embed.add_field(name="Your Score: "+str(user_score), value="** **", inline=True)
                embed.add_field(name="Bot Score: "+str(bot_score), value="** **", inline=True)
                embed.set_footer(text="First to reach "+str(games)+" points wins "+str(bet_amt)+" BE coins.\nType `exit` to leave the game.")
                await ctx.send(embed=embed)
            elif(user_choice_val == "scissors" and bot_choice_val=="rock"):
                bot_score = bot_score + 1
                embed=discord.Embed(title="Bot Gets a point", description="Bot Chose rock", color=discord.Color.blue())
                embed.add_field(name="Your Score: "+str(user_score), value="** **", inline=True)
                embed.add_field(name="Bot Score: "+str(bot_score), value="** **", inline=True)
                embed.set_footer(text="First to reach "+str(games)+" points wins "+str(bet_amt)+" BE coins.\nType `exit` to leave the game.")
                await ctx.send(embed=embed)
            elif(user_choice_val == "scissors" and bot_choice_val=="paper"):
                user_score = user_score + 1
                embed=discord.Embed(title="You Get a point!", description="Bot Chose paper", color=discord.Color.blue())
                embed.add_field(name="Your Score: "+str(user_score), value="** **", inline=True)
                embed.add_field(name="Bot Score: "+str(bot_score), value="** **", inline=True)
                embed.set_footer(text="First to reach "+str(games)+" points wins "+str(bet_amt)+" BE coins.\nType `exit` to leave the game.")
                await ctx.send(embed=embed)
            elif(user_choice_val == "scissors" and bot_choice_val=="scissors"):
                embed=discord.Embed(title="Same Choice", description="Bot Chose scissors", color=discord.Color.blue())
                embed.add_field(name="Your Score: "+str(user_score), value="** **", inline=True)
                embed.add_field(name="Bot Score: "+str(bot_score), value="** **", inline=True)
                embed.set_footer(text="First to reach "+str(games)+" points wins "+str(bet_amt)+" BE coins.\nType `exit` to leave the game.")
                await ctx.send(embed=embed)
            else:
                await ctx.send(ctx.author.mention+" Enter rock, paper or scissors only.\n(Type `exit` to leave the game)")

            if bot_score < user_score:
                c = user_score
            else:
                c = bot_score
        ## while loop end

        mydb = mysql.connector.connect(
        host=config.sql_host,
        user=config.sql_user,
        password=config.sql_pass,
        database=config.sql_db
        )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT money FROM user_data WHERE user_id='"+str(ctx.author.id)+"'")
        user_rpc_get = mycursor.fetchall()
        for user_rpc_data in user_rpc_get:
            user_bal = user_rpc_data[0]


        if(user_score < bot_score):
            winner = "bot"
            new_balance = user_bal - bet_amt
            update_rps_sql = "UPDATE `user_data` SET `money`="+str(new_balance)+" WHERE user_id = '"+str(ctx.author.id)+"'"
            mycursor.execute(update_rps_sql)
            mydb.commit()
            await ctx.send("\n**I win**. Better luck next time. (You lost "+str(bet_amt)+" BE coins)")
        else:
            winner="user"
            new_balance = user_bal + bet_amt
            update_rps_sql = "UPDATE `user_data` SET `money`="+str(new_balance)+" WHERE user_id = '"+str(ctx.author.id)+"'"
            mycursor.execute(update_rps_sql)
            mydb.commit()
            await ctx.send("\nCongrats! **You won!!** You got "+str(bet_amt)+" BE coins!")
        
        




        





###########################################  SEARCH  #######################################################


    @commands.command(name="search", brief="Search for BE coins", description="Search for BE coins")
    async def search(self, ctx):
        mydb = mysql.connector.connect(
        host=config.sql_host,
        user=config.sql_user,
        password=config.sql_pass,
        database=config.sql_db
        )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT search FROM user_data WHERE user_id='"+str(ctx.author.id)+"'")
        user_search_get = mycursor.fetchall()
        for user_search_data in user_search_get:
            user_search_time_a = user_search_data

        user_search_time_string = str(user_search_time_a).replace("(", "").replace(")", "").replace(",", "").replace("'", "")
        user_search_time = datetime.datetime.strptime(user_search_time_string, '%Y-%m-%d %H:%M:%S.%f')  

        mycursor.execute("SELECT money FROM user_data WHERE user_id='"+str(ctx.author.id)+"'")
        user_search_bal_get = mycursor.fetchall()
        for user_search_bal_data in user_search_bal_get:
            user_search_bal_a = user_search_bal_data 

        user_search_bal = int(str(user_search_bal_a).replace("(", "").replace(")", "").replace(",", "").replace("'", ""))

        current_time = datetime.datetime.now()

        search_cooldown = 30 
        user_search_diff = (current_time - user_search_time).total_seconds()


        if(user_search_diff >= search_cooldown):


            search_win_rate = (random.randint(1, 10))
            if(search_win_rate < 4):
                search_lose_lines = [
                    ' You robbed a poor man and got nothing.',
                    ' You tried robbing a bank and failed. The police is after you now',
                    ' You were searching in a sewer for BE coins and ended up falling in it.',
                    ' You went for searching BE coins in a plane and opened the wrong door falling from sky.'
                ]

                search_response = random.choice(search_lose_lines)
                outro = ""
                search_earn=""
                search_amt = 0

            else:
                search_earn = random.randint(60,710)
                search_amt = search_earn

                search_win_lines = [
                    ' You opened your purse and found ',
                    ' You broke your piggy bank and found ',
                    ' You broke into your neighbours car and found ',
                    ' You robbed a man walking in the streets and got ',
                    ' You searched in your house and found ',
                    ' You looked under your sofa and found ',
                    ' You climned up a tree and found '

                ]
                search_response = random.choice(search_win_lines)
                outro = " BE coins!"
            
            await ctx.channel.send(ctx.author.mention + search_response + str(search_earn) + outro)

            user_search_final_bal = user_search_bal + search_amt

            update_search_sql= "UPDATE `user_data` SET `money` = '"+str(user_search_final_bal)+"', `search`='"+str(current_time)+"' WHERE user_id = '"+str(ctx.author.id)+"'"
            mycursor.execute(update_search_sql)
            mydb.commit()
        else:
            await ctx.channel.send(ctx.author.mention+" You can use this command again after "+str(30 - (round(user_search_diff)))+" seconds")


###################################################  BEG  ###########################################################


    @commands.command(name="beg", brief="Beg for BE coins", description="Beg for BE coins")
    async def beg(self, ctx):
        mydb = mysql.connector.connect(
        host=config.sql_host,
        user=config.sql_user,
        password=config.sql_pass,
        database=config.sql_db
        )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT beg FROM user_data WHERE user_id='"+str(ctx.author.id)+"'")
        user_beg_get = mycursor.fetchall()
        for user_beg_data in user_beg_get:
            user_beg_time_a = user_beg_data

        user_beg_time_string = str(user_beg_time_a).replace("(", "").replace(")", "").replace(",", "").replace("'", "")
        user_beg_time = datetime.datetime.strptime(user_beg_time_string, '%Y-%m-%d %H:%M:%S.%f')  

        mycursor.execute("SELECT money FROM user_data WHERE user_id='"+str(ctx.author.id)+"'")
        user_beg_bal_get = mycursor.fetchall()
        for user_beg_bal_data in user_beg_bal_get:
            user_beg_bal_a = user_beg_bal_data 

        user_beg_bal = int(str(user_beg_bal_a).replace("(", "").replace(")", "").replace(",", "").replace("'", ""))

        current_time = datetime.datetime.now()

        beg_cooldown = 30 
        user_beg_diff = (current_time - user_beg_time).total_seconds()


        if(user_beg_diff >= beg_cooldown):


            beg_win_rate = (random.randint(1, 10))
            if(beg_win_rate < 4):
                beg_lose_lines = [
                    ' "You poor begger go get a job." - street pedestrian',
                    ' "I hate beggers" - some person',
                    ' "Stop begging in the streets" - shop owner',
                    ' "I will not give any money to a lazy begger" - rich man'
                ]

                beg_response = random.choice(beg_lose_lines)
                outro = ""
                beg_earn=""
                beg_amt = 0

            else:
                beg_earn = random.randint(60,710)
                beg_amt = beg_earn

                beg_win_lines = [
                    ' An old man gave you ',
                    ' You begged in the streets and got ',
                    ' A rich man gave you ',
                    ' You started begging in a shop and got ',
                    ' You were begging in a museum and got ',
                    ' You were begging to a tree and suddenly you got ',
                    ' You started begging in the roads and got '

                ]
                beg_response = random.choice(beg_win_lines)
                outro = " BE coins!"
            
            await ctx.channel.send(ctx.author.mention + beg_response + str(beg_earn) + outro)

            user_beg_final_bal = user_beg_bal + beg_amt

            update_beg_sql= "UPDATE `user_data` SET `money` = '"+str(user_beg_final_bal)+"', `beg`='"+str(current_time)+"' WHERE user_id = '"+str(ctx.author.id)+"'"
            mycursor.execute(update_beg_sql)
            mydb.commit()
        else:
            await ctx.channel.send(ctx.author.mention+" You can use this command again after "+str(30 - (round(user_beg_diff)))+" seconds")


###################################################  HUNT  #######################################################################

    @commands.command(name="hunt", brief="hunt animals", description="Hunt down animals and sell them for BE coins")
    async def hunt(self, ctx):
        mydb = mysql.connector.connect(
        host=config.sql_host,
        user=config.sql_user,
        password=config.sql_pass,
        database=config.sql_db
        )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT bow FROM user_data WHERE user_id='"+str(ctx.author.id)+"'")
        user_bow_get = mycursor.fetchall()
        for user_bow_data in user_bow_get:
            user_bow = user_bow_data[0]
        
        if user_bow != 0:

            mycursor.execute("SELECT hunt FROM user_data WHERE user_id='"+str(ctx.author.id)+"'")
            user_hunt_get = mycursor.fetchall()
            for user_hunt_data in user_hunt_get:
                user_hunt_time_a = user_hunt_data[0]

            user_hunt_time = datetime.datetime.strptime(user_hunt_time_a, '%Y-%m-%d %H:%M:%S.%f')  

            mycursor.execute("SELECT boar FROM user_data WHERE user_id='"+str(ctx.author.id)+"'")
            user_boar_bal_get = mycursor.fetchall()
            for user_boar_bal_data in user_boar_bal_get:
                user_boar = user_boar_bal_data[0]

            user_boar_quan = int(user_boar)

            current_time = datetime.datetime.now()

            hunt_cooldown = 30 
            user_hunt_diff = (current_time - user_hunt_time).total_seconds()


            if(user_hunt_diff >= hunt_cooldown):


                hunt_win_rate = (random.randint(1, 10))
                if(hunt_win_rate < 4):
                    hunt_lose_lines = [
                        ' You went for hunting a bear and right when it started charging on you, you realise your arrows are over. ',
                        ' You went for hunting and found nothing',
                        ' Your bow slipped from your hand while hunting a deer. You got nothing ',
                        ' You went for hunting in the woods and found slenderman.'
                    ]

                    hunt_response = random.choice(hunt_lose_lines)
                    boar_amt = 0

                else:

                    hunt_response = "You went hunting and found 1 boar!"
                    boar_amt=1
                
                await ctx.channel.send(ctx.author.mention + hunt_response)

                user_boar_final_quan = user_boar_quan + boar_amt

                update_hunt_sql= "UPDATE `user_data` SET `boar` = '"+str(user_boar_final_quan)+"', `hunt`='"+str(current_time)+"' WHERE user_id = '"+str(ctx.author.id)+"'"
                mycursor.execute(update_hunt_sql)
                mydb.commit()
            else:
                await ctx.channel.send(ctx.author.mention+" You can use this command again after "+str(30 - (round(user_hunt_diff)))+" seconds")

        else:
            await ctx.send("You do not have a bow to hunt animals.. Buy a bow from the BE shop")

    


def setup(client):
    client.add_cog(Games(client))