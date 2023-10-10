# Currency Cog for BE Bot
# Author: BraxtonElmer

import discord
from discord.ext import commands
import random
import mysql.connector
import datetime
import config

class Currency(commands.Cog):
    """be help Currency"""

    def __init__(self, client):
        self.client = client

    # #events
    # @commands.Cog.listener()
    # async def on_ready(self):
    #     print("Currency cogs online")
    

    #commands

#########################################  BALANCE  ###############################################

    @commands.command(name="bal", brief="Shows BE coins Balance of user", description="Shows BE coins Balance of user", usage="<user>", aliases=['balance'])
    async def bal(self, ctx, member: discord.Member=None):
        if(member == None):
            member_bal = ctx.author
        else:
            member_bal = member

        bot_info=self.client.user

        mydb = mysql.connector.connect(
        host=config.sql_host,
        user=config.sql_user,
        password=config.sql_pass,
        database=config.sql_db
        )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT money, locker, locker_limit FROM user_data WHERE username='"+str(member_bal).replace("'", "\\'")+"'")
        user_bal_get = mycursor.fetchall()
        for user_bal_data in user_bal_get:
            user_bal = user_bal_data[0]
            user_locker_bal = user_bal_data[1]
            user_locker_limit = user_bal_data[2]

        if(member == None):
            embed=discord.Embed(title=ctx.author.name+"'s Balance:", description= "**Wallet:** "+'{:,}'.format(user_bal)+" BE coins\n**Locker:** "+'{:,}'.format(user_locker_bal)+" / "+'{:,}'.format(user_locker_limit)+" BE coins", color=discord.Color.gold())
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        elif(member == bot_info):
            embed=discord.Embed(title="You are seeing my balance? :smirk:", description= "I have infinte BE coins!!", color=discord.Color.gold())
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title=str(member_bal)+"'s Balance:", description= "**Wallet:** "+'{:,}'.format(user_bal)+" BE coins\n**Locker:** "+'{:,}'.format(user_locker_bal)+" / "+'{:,}'.format(user_locker_limit)+" BE coins", color=discord.Color.gold())
            embed.set_author(name=str(member_bal), icon_url=member_bal.avatar_url)
            await ctx.send(embed=embed)



####################################  GIVE  #########################################################################

    @commands.command(name="give", brief="Give BE coins to other users.", description="Gives other users BE coins", usage="<user> <BE coins>")
    async def give(self, ctx,  member: discord.Member=None, give_amt=None, dm=""):
        if(member == None):
            await ctx.send("Mention an user to give BE coins.\nSyntax: `be give <BE coins> <user>`")
            return
        elif(give_amt == None):
            await ctx.send("Mention BE coins to give to user.\nSyntax: `be give <BE coins> <user>`")
            return
        elif(ctx.author.name == member.name):
            await ctx.send("You cant give BE coins to yourself!")
            return
        
        
        mydb = mysql.connector.connect(
        host=config.sql_host,
        user=config.sql_user,
        password=config.sql_pass,
        database=config.sql_db
        )
        mycursor = mydb.cursor()

        #sender
        mycursor.execute("SELECT money FROM user_data WHERE user_id='"+str(ctx.author.id)+"'")
        sender_bal_get = mycursor.fetchall()
        for give_sender_bal_data in sender_bal_get:
            give_sender_bal = give_sender_bal_data
            sender_bal = int(str(give_sender_bal).replace("(", "").replace(")", "").replace(",", "")) 
        if sender_bal < int(give_amt):
            await ctx.send(ctx.author.mention+" You have below "+str(give_amt)+" in you Balance. Transaction Failed.")
            return

        #receiver
        mycursor.execute("SELECT money FROM user_data WHERE user_id='"+str(member.id)+"'")
        reciever_bal_get = mycursor.fetchall()
        for give_reciever_bal_data in reciever_bal_get:
            give_reciever_bal = give_reciever_bal_data
            reciever_bal = int(str(give_reciever_bal).replace("(", "").replace(")", "").replace(",", "")) 

        new_reciever_balance = reciever_bal + int(give_amt)
        new_sender_balance = sender_bal - int(give_amt)

        #sender
        update_sender_sql = "UPDATE `user_data` SET `money`="+str(new_sender_balance)+" WHERE user_id = '"+str(ctx.author.id)+"'"
        mycursor.execute(update_sender_sql)
        mydb.commit()

        #reciever
        update_reciever_sql = "UPDATE `user_data` SET `money`="+str(new_reciever_balance)+" WHERE user_id = '"+str(member.id)+"'"
        mycursor.execute(update_reciever_sql)
        mydb.commit()
        await ctx.send(ctx.author.mention+" Successfully gave "+str(give_amt)+" BE coins to "+str(member))
        if(dm == "server-vote" and ctx.author.id == config.dev_user_id):
            await member.send("You have been given "+str(give_amt)+" BE coins for voting for our Server! Thank you!")
        elif(dm == "bot-vote" and ctx.author.id == config.dev_user_id):
            await member.send("You have been given "+str(give_amt)+" BE coins for voting for our bot! Thank you!")
        else:
            await member.send(str(ctx.author.name)+" gave you "+str(give_amt)+" BE coins")




#####################################################  RICH  ########################################################################


    @commands.command(name="rich", brief="See richest users in the server", description="Shows the richest users in the server having BE coins.")
    async def rich(self, ctx):
        mydb = mysql.connector.connect(
        host=config.sql_host,
        user=config.sql_user,
        password=config.sql_pass,
        database=config.sql_db
        )
        mycursor = mydb.cursor()
        users =""
        async for member in ctx.guild.fetch_members(limit=None):
            users=users+"'"+str(member.id)+"', "

        all_users = users[:-2]
        mycursor.execute("SELECT money, username FROM user_data WHERE money NOT IN (150, 100) AND user_id IN ("+all_users+") ORDER BY money DESC LIMIT 5;")
        user_rich_get = mycursor.fetchall()
        rich_users=""
        ij=0
        for user_rich_data in user_rich_get:
            if(ij==0):
                medal = ":first_place:"
            elif(ij==1):
                medal=":second_place:"
            elif(ij==2):
                medal=":third_place:"
            elif(ij==3):
                medal=":medal:"
            else:
                medal=":military_medal:"
            rich_users = rich_users+medal+" **"+'{:,}'.format(user_rich_data[0])+"** :- "+user_rich_data[1]+"\n"
            ij = ij+1

        embed=discord.Embed(title="Richest users in "+ctx.guild.name, description= rich_users, color=discord.Color.blue())
        embed.set_footer(text="This is wallet and not Net worth")
        await ctx.send(embed=embed)

###########################################################  SELL  ####################################################################3333#

    @commands.command(name="sell", brief="sell animals you hunted for BE coins", description="Sell animals you hunted for BE coins", usage="<animal> <quantity (optional)>")
    async def sell(self, ctx, animal=None, quantity="none"):
        if(animal == None):
            await ctx.send("Mention an animal to sell.")
            return

        if(animal == "boar"):   ## add or statement for other animals
            mydb = mysql.connector.connect(
            host=config.sql_host,
            user=config.sql_user,
            password=config.sql_pass,
            database=config.sql_db
            )
            mycursor = mydb.cursor()
            mycursor.execute("SELECT money, boar FROM user_data WHERE user_id='"+str(ctx.author.id)+"'")
            user_animal_get = mycursor.fetchall()
            for user_animal_data in user_animal_get:
                user_bal = user_animal_data[0]
                user_boar = user_animal_data[1]

            if user_boar != 0:

                if str(quantity) == "max" or str(quantity) == "all":
                    quantity = user_boar
                else:
                    if(quantity.isnumeric()):
                        quantity = int(quantity)
                    else:
                        quantity = 1
                new_animal_quantity = user_boar - quantity
                sell_val = 200 * quantity
                new_bal = user_bal + sell_val
                animal = "boar"

            else:
                await ctx.send("You do not have this item.")
                return

            update_animalhunt_sql= "UPDATE `user_data` SET `money` = "+str(new_bal)+", `boar` = "+str(new_animal_quantity)+" WHERE user_id = '"+str(ctx.author.id)+"'"
            mycursor.execute(update_animalhunt_sql)
            mydb.commit()

            await ctx.send(ctx.author.mention+" You sold "+str(quantity)+" "+animal+" and got "+str(sell_val)+" BE coins!")

            


############################################################   DEPOSIT   #################################################################

    @commands.command(name="dep", brief="Deposit BE coins to your locker", description="Deposit BE coins to your locker", usage="<BE coins>", aliases=['deposit'])
    async def dep(self, ctx, dep_amt="none"):
        mydb = mysql.connector.connect(
        host=config.sql_host,
        user=config.sql_user,
        password=config.sql_pass,
        database=config.sql_db
        )
        mycursor = mydb.cursor()

        #sender
        mycursor.execute("SELECT money, locker, locker_limit FROM user_data WHERE user_id='"+str(ctx.author.id)+"'")
        dep_get = mycursor.fetchall()
        for dep_data in dep_get:
            user_bal = dep_data[0]
            locker_bal = dep_data[1]
            locker_limit = dep_data[2]

        if(str(dep_amt) == "none"):
            await ctx.send(ctx.author.mention+" Mention BE coins to deposit in locker.\nSyntax: `be dep <BE coins>`")
            return
        elif(str(dep_amt) == "max" or str(dep_amt)=="all"):
            dep_amt= locker_limit-locker_bal
            if(dep_amt > user_bal):
                dep_amt = user_bal

        if(locker_bal == locker_limit):
            await ctx.send(ctx.author.mention+" You have a full locker!\n**HINT:** You can get safenotes from other currency commands like hunt and fish or for voting which you can use to extend your locker space!")
            return
        
        new_balance = int(user_bal) - int(dep_amt)
        new_locker = int(locker_bal) + int(dep_amt)


        update_dep_sql = "UPDATE `user_data` SET `money`="+str(new_balance)+", locker="+str(new_locker)+" WHERE user_id = '"+str(ctx.author.id)+"'"
        mycursor.execute(update_dep_sql)
        mydb.commit()


        await ctx.send(ctx.author.mention+" You have kept "+str(dep_amt)+" BE coins in your locker!")

    @dep.error
    async def dep_error(self, ctx, error):
        await ctx.send(ctx.author.mention+" Mention BE coins to deposit in locker.\nSyntax: `be dep <BE coins>`")



    @commands.command(name="withdraw", brief="withosit BE coins to your locker", description="withosit BE coins to your locker", usage="<BE coins>", aliases=['with'])
    async def withdraw(self, ctx, with_amt="none"):
        mydb = mysql.connector.connect(
        host=config.sql_host,
        user=config.sql_user,
        password=config.sql_pass,
        database=config.sql_db
        )
        mycursor = mydb.cursor()

        #sender
        mycursor.execute("SELECT money, locker FROM user_data WHERE user_id='"+str(ctx.author.id)+"'")
        with_get = mycursor.fetchall()
        for with_data in with_get:
            user_bal = with_data[0]
            locker_bal = with_data[1]

        if(str(with_amt) == "none"):
            await ctx.send(ctx.author.mention+" Mention BE coins to withdraw from locker.\nSyntax: `be with <BE coins>`")
            return
        elif(str(with_amt) == "max" or str(with_amt)=="all"):
            with_amt= locker_bal
        elif(with_amt.isnumeric()):
            with_amt = int(with_amt)
        else:
            await ctx.send(ctx.author.mention+" Mention BE coins to withdraw from locker.\nSyntax: `be with <BE coins>`")

        if(with_amt > locker_bal):
            await ctx.send(ctx.author.mention+" You do not have "+str(with_amt)+" BE coins in your locker.")
            return
        
        new_balance = int(user_bal) + int(with_amt)
        new_locker = int(locker_bal) - int(with_amt)


        update_with_sql = "UPDATE `user_data` SET `money`="+str(new_balance)+", locker="+str(new_locker)+" WHERE user_id = '"+str(ctx.author.id)+"'"
        mycursor.execute(update_with_sql)
        mydb.commit()


        await ctx.send(ctx.author.mention+" You have withdrawn "+str(with_amt)+" BE coins from your locker!")

    # @withdraw.error
    # async def with_error(self, ctx, error):
    #     await ctx.send(ctx.author.mention+" Mention BE coins to withdraw from locker.\nSyntax: `be with <BE coins>`")


            
        



def setup(client):
    client.add_cog(Currency(client))