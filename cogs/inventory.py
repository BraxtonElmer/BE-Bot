# Inventory Cog for BE Bot
# Author: BraxtonElmer

import discord
from discord.ext import commands
import random
import mysql.connector
import config

class Inventory(commands.Cog):
    """be help Inventory"""

    def __init__(self, client):
        self.client = client


######################################  MAIL  ##########################################################

    # @commands.command(name="mail", brief="Check mail for voting rewards", description="See available stuff from BE shop")
    # async def shop(self, ctx, collect=None):
    #     mydb = mysql.connector.connect(

    #     )
    #     mycursor = mydb.cursor()
    #     mycursor.execute("SELECT money, safenote FROM user_data WHERE user_id='"+str(ctx.author.id)+"'")
    #     mail_get = mycursor.fetchall()
    #     for mail_data in mail_get:
    #         money_mail = mail_data[0]
    #         safenote_mail = mail_data[1]
    #     await ctx.send("You currently have "+str(money_mail)+" BE coins and "+str(safenote_mail)+" safenotes in your mail.. Use `be mail claim` to claim all rewards.")
    #     mydb.close()
        







########################################   SHOP   ###########################################################

    @commands.command(name="shop", brief="See available stuff from BE shop", description="See available stuff from BE shop")
    async def shop(self, ctx, item=None):
        if(item == None):
            embed=discord.Embed(title="BE shop", description= "Buy stuff from BE shop!", color=discord.Color.magenta())
            embed.add_field(name=":pizza: Pizza - 2000 BE coins", value="Eat a pizza and if you are lucky you may get BE coins\n(ID: pizza)", inline=False)
            embed.add_field(name=":apple: Apple - 3000 BE coins", value="An apple a day keeps the doctor away. If you eat it you won't die for 24 hours.\n(ID: apple)", inline=False)
            embed.add_field(name=":candy: Lucky Candy - 5000 BE coins", value="Get a chance to increase your luck rate upto 10% for 10 minutes\n(ID: lucky-candy)", inline=False)
            embed.add_field(name=":bow_and_arrow: Bow - 10,000 BE coins", value="Use a bow to hunt animals.\n(ID: bow)", inline=False)
            embed.set_footer(text="See `be help use` for using stuff bought from shop. (Lucky candy is currently unavailable.)")
            await ctx.send(embed=embed)

        elif(item == "pizza"):
            embed=discord.Embed(title="Pizza", description= "You can eat a pizza and if you are lucky you may get some BE coins from 500 - 3000 per pizza.", color=discord.Color.magenta())
            embed.add_field(name="Buy", value="2000 BE coins", inline=False)
            embed.add_field(name="ID", value="pizza", inline=False)
            await ctx.send(embed=embed)

        elif(item == "apple"):
            embed=discord.Embed(title="Apple", description= "You can eat an apple which will prevent your death in the next 24 hours, so you wont lose all your money in your wallet.", color=discord.Color.magenta())
            embed.add_field(name="Buy", value="3000 BE coins", inline=False)
            embed.add_field(name="ID", value="apple", inline=False)
            await ctx.send(embed=embed)

        elif(item == "lucky-candy"):
            embed=discord.Embed(title="Bow", description= "You can eat a lucky candy and you may or may not get a luck rate upto 10% for getting BE coins.", color=discord.Color.magenta())
            embed.add_field(name="Buy", value="5000 BE coins", inline=False)
            embed.add_field(name="ID", value="lucky-candy", inline=False)
            await ctx.send(embed=embed)            

        elif(item == "bow"):
            embed=discord.Embed(title="Bow", description= "You can use a bow to hunt animals down, which you can sell for BE coins.", color=discord.Color.magenta())
            embed.add_field(name="Buy", value="10000 BE coins", inline=False)
            embed.add_field(name="ID", value="bow", inline=False)
            await ctx.send(embed=embed)

        else:
            await ctx.send("Item does not exist in shop or out of stock")

#######################################    BUY    ####################################################

    @commands.command(name="buy", brief="Buy stuff from BE shop", description="Buy stuff from BE shop", usage="<item> <quantity (optional)>")
    async def buy(self, ctx, item=None, quantity=1):
        if item == None:
            await ctx.send("Mention an Item to buy from the shop. To see available items use `be shop` command.")
            return
 
        
        ####################  BUY PIZZA  ##################################


        elif item == "pizza": 
            mydb = mysql.connector.connect(
            host=config.sql_host,
            user=config.sql_user,
            password=config.sql_pass,
            database=config.sql_db  
            )
            mycursor = mydb.cursor()
            mycursor.execute("SELECT money FROM user_data WHERE user_id='"+str(ctx.author.id)+"'")
            user_bal_get = mycursor.fetchall()
            for user_bal_data in user_bal_get:
                user_bal = user_bal_data
                user_bal_string = str(user_bal).replace("(", "").replace(")", "").replace(",", "") 
            if int(user_bal_string) <= (2000*quantity):
                await ctx.send("You do not have enough BE coins to buy "+str(quantity)+" pizza(s)")
                return
            else:
                mycursor.execute("SELECT pizza FROM user_data WHERE user_id='"+str(ctx.author.id)+"'")
                user_pizza_get = mycursor.fetchall()
                for user_pizza_data in user_pizza_get:
                    user_pizza = user_pizza_data
                    user_pizza_string = str(user_pizza).replace("(", "").replace(")", "").replace(",", "") 

                new_pizza_quantity = int(user_pizza_string) + quantity
                new_user_bal = int(user_bal_string) - (2000*quantity)
                update_user_inv = "UPDATE `user_data` SET `money`='"+str(new_user_bal)+"', `pizza`="+str(new_pizza_quantity)+" WHERE user_id = '"+str(ctx.author.id)+"'"
                mycursor.execute(update_user_inv)
                mydb.commit()

                embed=discord.Embed(description= "Your just bought "+str(quantity)+" pizza(s) for "+str(2000*quantity)+" BE coins", color=discord.Color.gold())
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                embed.set_footer(text="Thank you for buying from BE shop!")
                await ctx.send(embed=embed)


            ######################  BUY APPLE  ######################


        elif item == "apple":
            mydb = mysql.connector.connect(
            host=config.sql_host,
            user=config.sql_user,
            password=config.sql_pass,
            database=config.sql_db
            )
            mycursor = mydb.cursor()
            mycursor.execute("SELECT money FROM user_data WHERE user_id='"+str(ctx.author.id)+"'")
            user_bal_get = mycursor.fetchall()
            for user_bal_data in user_bal_get:
                user_bal = user_bal_data
                user_bal_string = str(user_bal).replace("(", "").replace(")", "").replace(",", "") 


            if int(user_bal_string) <= (3000*quantity):
                await ctx.send("You do not have enough BE coins to buy "+str(quantity)+" apple(s)")
                return
            else:
                mycursor.execute("SELECT apple FROM user_data WHERE user_id='"+str(ctx.author.id)+"'")
                user_apple_get = mycursor.fetchall()
                for user_apple_data in user_apple_get:
                    user_apple = user_apple_data
                    user_apple_string = str(user_apple).replace("(", "").replace(")", "").replace(",", "") 

                new_apple_quantity = int(user_apple_string) + quantity
                new_user_bal = int(user_bal_string) - (3000*quantity)
                update_user_inv = "UPDATE `user_data` SET `money`='"+str(new_user_bal)+"', `apple`="+str(new_apple_quantity)+" WHERE user_id = '"+str(ctx.author.id)+"'"
                mycursor.execute(update_user_inv)
                mydb.commit()

                embed=discord.Embed(description= "Your just bought "+str(quantity)+" apple(s) for "+str(3000*quantity)+" BE coins", color=discord.Color.gold())
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                embed.set_footer(text="Thank you for buying from BE shop!")
                await ctx.send(embed=embed)


                #########   BUY BOW  #############

        elif item == "bow":
            mydb = mysql.connector.connect(
            host=config.sql_host,
            user=config.sql_user,
            password=config.sql_pass,
            database=config.sql_db
            )
            mycursor = mydb.cursor()
            mycursor.execute("SELECT money FROM user_data WHERE user_id='"+str(ctx.author.id)+"'")
            user_bal_get = mycursor.fetchall()
            for user_bal_data in user_bal_get:
                user_bal = user_bal_data[0]


            if user_bal <= (10000*quantity):
                await ctx.send("You do not have enough BE coins to buy "+str(quantity)+" bow(s)")
                return
            else:
                mycursor.execute("SELECT bow FROM user_data WHERE user_id='"+str(ctx.author.id)+"'")
                user_bow_get = mycursor.fetchall()
                for user_bow_data in user_bow_get:
                    user_bow = user_bow_data[0]

                new_bow_quantity = user_bow + quantity
                new_user_bal = user_bal - (10000*quantity)
                update_user_inv = "UPDATE `user_data` SET `money`='"+str(new_user_bal)+"', `bow`="+str(new_bow_quantity)+" WHERE user_id = '"+str(ctx.author.id)+"'"
                mycursor.execute(update_user_inv)
                mydb.commit()

                embed=discord.Embed(description= "Your just bought "+str(quantity)+" bow(s) for "+str(10000*quantity)+" BE coins", color=discord.Color.gold())
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                embed.set_footer(text="Thank you for buying from BE shop!")
                await ctx.send(embed=embed)


        else:
            await ctx.send("The item you mentioned does not exist. To see available items use `be shop` command.")

    @commands.command(name="use", brief="Use items which were bought from BE shop", description="Use items which were bought from BE shop", usage="<item> <quantity (optional)>")
    async def use(self, ctx, item=None, quantity="none"):
        if item == None:
            ctx.send("Mention an item to use. Syntax: `be use <item> <quantity (optional)>")
            return

        ######################  EAT PIZZA  ##################


        elif item == "pizza":
            mydb = mysql.connector.connect(
            host=config.sql_host,
            user=config.sql_user,
            password=config.sql_pass,
            database=config.sql_db
            )
            mycursor = mydb.cursor()
            mycursor.execute("SELECT money, pizza FROM user_data WHERE user_id='"+str(ctx.author.id)+"'")
            user_gift_bal_get = mycursor.fetchall()
            for user_gift_bal_data in user_gift_bal_get:
                gift_bal = user_gift_bal_data[0]
                pizza_bal = user_gift_bal_data[1]
            if str(quantity) == "max" or str(quantity) == "all":
                quantity = pizza_bal
            else:
                if(quantity.isnumeric()):
                    quantity = int(quantity)
                else:
                    quantity = 1
                
            if pizza_bal !=0:
                money_earned = random.randint(500,3000)
                i=1
                while(i<quantity):
                    money_earned = money_earned + random.randint(500,3000)
                    i = i+1
                new_pizza_bal = int(pizza_bal) - quantity
                new_gift_bal = money_earned + gift_bal
                gift_bal_sql = "UPDATE `user_data` SET `money`="+str(new_gift_bal)+", `pizza`="+str(new_pizza_bal)+" WHERE user_id = '"+str(ctx.author.id)+"'"
                mycursor.execute(gift_bal_sql)
                mydb.commit()
                await ctx.send(ctx.author.mention+" You eat "+str(quantity)+" pizza and find "+str(money_earned)+" in the box!!")
            else:
                await ctx.send("You do not have pizza in your inventory.")


        elif item == "safenote":
            mydb = mysql.connector.connect(
            host=config.sql_host,
            user=config.sql_user,
            password=config.sql_pass,
            database=config.sql_db
            )
            mycursor = mydb.cursor()
            mycursor.execute("SELECT locker_limit, safenote FROM user_data WHERE user_id='"+str(ctx.author.id)+"'")
            user_gift_bal_get = mycursor.fetchall()
            for user_gift_bal_data in user_gift_bal_get:
                gift_bal = user_gift_bal_data[0]
                safenote_bal = user_gift_bal_data[1]                


            if safenote_bal !=0:

                if str(quantity) == "max" or str(quantity) == "all":
                    quantity = safenote_bal
                else:
                    if(quantity.isnumeric()):
                        quantity = int(quantity)
                    else:
                        if(safenote_bal > 1):
                            await ctx.send(ctx.author.mention+" You have "+str(safenote_bal)+" :pager: Safenotes. How many do you want to use now?")
                            def check(m):
                                return m.author == ctx.author and m.channel == ctx.channel
                            reply = await self.client.wait_for('message', check=check)
                            if(reply.content.isnumeric()):
                                quantity = int(reply.content)
                            else:
                                await ctx.send(ctx.author.mention+" You did not enter a valid number.")
                                return
                            if quantity > safenote_bal:
                                await ctx.send(ctx.author.mention+" You do not have "+str(quantity)+" :pager: Safenotes.")
                                return
                        else:
                            quantity = 1


                money_earned = random.randint(5000,7000)
                i=1
                while(i<quantity):
                    money_earned = money_earned + random.randint(5000,7000)
                    i = i+1
                new_safenote_bal = int(safenote_bal) - quantity
                new_locker_bal = money_earned + gift_bal
                gift_bal_sql = "UPDATE `user_data` SET `locker_limit`="+str(new_locker_bal)+", `safenote`="+str(new_safenote_bal)+" WHERE user_id = '"+str(ctx.author.id)+"'"
                mycursor.execute(gift_bal_sql)
                mydb.commit()
                await ctx.send(ctx.author.mention+" You use :pager: "+str(quantity)+" safenote and increase your locker space by "+str(money_earned)+"!")
            else:
                await ctx.send("You do not have safenote in your inventory.")

        elif item == "bow":
            await ctx.send(ctx.author.mention+" You cannot use this item.")

        elif item == "lucky-candy":
            await ctx.send("You have immunity already.")

        else:
            await ctx.send("The item you mentioned does not exist.")



    @commands.command(name="inv", brief="See your inventory", description="See all the stuff you bought from BE shop", usage="", aliases=['inventory'])
    async def inv(self, ctx, item=None, quantity=1):
        mydb = mysql.connector.connect(
        host=config.sql_host,
        user=config.sql_user,
        password=config.sql_pass,
        database=config.sql_db
        )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT pizza, apple, bow, safenote, boar FROM user_data WHERE user_id="+str(ctx.author.id)+"")
        user_get = mycursor.fetchall()
        for row in user_get:
            pizza_quantity = row[0]
            apple_quantity = row[1]
            bow_quantity = row[2]
            safenote_quantity = row[3]
            boar_quantity = row[4]

        if pizza_quantity == 0 and apple_quantity ==0 and bow_quantity == 0 and safenote_quantity == 0:
            await ctx.send("You have nothing in your inventory.")
            return
        else:
            embed=discord.Embed(title="Inventory:",  color=discord.Color.magenta())
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        if pizza_quantity != 0:
            embed.add_field(name=":pizza: Pizza - "+str(pizza_quantity), value="Item type: Powerup, consumable", inline=False)
        if apple_quantity !=0:
            embed.add_field(name=":apple: Apple - "+str(apple_quantity), value="Item type: Powerup, consumable", inline=False)
        if bow_quantity !=0:
            embed.add_field(name=":bow_and_arrow: Bow - "+str(bow_quantity), value="Item type: Tool", inline=False)
        if boar_quantity !=0:
            embed.add_field(name=":boar: Boar - "+str(boar_quantity), value="Item type: Sellable", inline=False)
        if safenote_quantity !=0:
            embed.add_field(name=":pager: safenote - "+str(safenote_quantity), value="Item type: Tool", inline=False)

        embed.set_footer(text="See 'be help use' for using items.")
        await ctx.send(embed=embed)
        



def setup(client):
    client.add_cog(Inventory(client))