import discord
from discord.ext import commands
import config
import mysql.connector
import datetime
import time

start_time = time.time()

class Misc(commands.Cog):
    """be help Misc"""

    def __init__(self, client):
        self.client = client

    @commands.command(name="vote", brief="Shows BE coins Balance of user", description="Shows BE coins Balance of user", usage="")
    async def vote(self, ctx):
        mydb = mysql.connector.connect(
        host=config.sql_host,
        user=config.sql_user,
        password=config.sql_pass,
        database=config.sql_db
        )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT server_vote, dbl_vote, topgg_vote FROM user_data WHERE user_id='"+str(ctx.author.id)+"'")
        user_vote_get = mycursor.fetchall()
        for user_vote_data in user_vote_get:
            user_server_vote_time = user_vote_data[0]
            user_dbl_vote_time = user_vote_data[1]
            user_topgg_vote_time = user_vote_data[2]

        current_time = datetime.datetime.now().replace(microsecond=0)        
        user_server_vote = datetime.datetime.strptime(user_server_vote_time, '%Y-%m-%d %H:%M:%S')  
        user_dbl_vote = datetime.datetime.strptime(user_dbl_vote_time, '%Y-%m-%d %H:%M:%S') 
        user_topgg_vote = datetime.datetime.strptime(user_topgg_vote_time, '%Y-%m-%d %H:%M:%S') 
        vote_cooldown = datetime.timedelta(hours=12) 
        user_server_vote_diff = (current_time - user_server_vote) 
        user_dbl_vote_diff = (current_time - user_dbl_vote)
        user_topgg_vote_diff = (current_time - user_topgg_vote)
        dbl_vote_cooldown = False
        server_vote_cooldown = False
        topgg_vote_cooldown = False
        if(user_dbl_vote_diff <= vote_cooldown):
            dbl_vote_cooldown = True
        if(user_server_vote_diff <= vote_cooldown):
            server_vote_cooldown = True
        if(user_topgg_vote_diff <= vote_cooldown):
            topgg_vote_cooldown = True

        embed=discord.Embed(title="Vote for BE Bot", description= "** **", color=discord.Color.magenta())   
        if topgg_vote_cooldown == True:
            embed.add_field(name="**top.gg**", value="`Time Remaining: "+str(vote_cooldown - user_topgg_vote_diff)+"`", inline=False)
        else:
            embed.add_field(name="**top.gg**", value="[`Vote Now!`](https://top.gg/bot/839120039218774016/vote)", inline=False)
        if dbl_vote_cooldown == True:
            embed.add_field(name="**discordbotlist.com**", value="`Time Remaining: "+str(vote_cooldown - user_dbl_vote_diff)+"`", inline=False)
        else:
            embed.add_field(name="**discordbotlist.com**", value="[`Vote Now!`](https://discordbotlist.com/bots/be-bot/upvote)", inline=False)
        
        if(ctx.guild.id == 577073465304154115 or ctx.guild.id== 778465731788537876):
            embed.add_field(name="------------------------", value="** **", inline=False)
            if server_vote_cooldown == True:
                embed.add_field(name="**top.gg servers**", value="`Time Remaining: "+str(vote_cooldown - user_server_vote_diff)+"`", inline=False)
            else:
                embed.add_field(name="**top.gg servers**", value="[`Vote Now!`](https://top.gg/servers/577073465304154115/vote)", inline=False)

        embed.add_field(name="Rewards:", value="10,000 BE coins\n:pager: 5 safenote", inline=False)
        embed.add_field(name="**NOTE: You will receive your rewards as soon as you vote!**", value="** **", inline=False)
        await ctx.send(embed=embed)    


    @commands.command(name="ping", brief="Shows the ping of bot", description="Shows the ping of bot")
    async def ping(self, ctx):
        await ctx.send(f'Ping of bot is: {round(self.client.latency * 1000)} ms')

    def is_it_dev(ctx):
        return ctx.author.id == config.dev_user_id

    @commands.command()
    @commands.check(is_it_dev)
    async def say(self, ctx, *, sentence):
        await ctx.message.delete()
        await ctx.send(sentence)


    @commands.command(name='user', brief='Get information about a user', description='Get information of a user by pinging them. Not passing any ping will show your own information.')
    @commands.check(is_it_dev)
    async def whois(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author

        embed = discord.Embed(
        title = 'User Information',
        description = f'User Information for {member.display_name}',
        colour = member.color
        )

        embed.set_thumbnail(url = member.avatar_url)
    
        embed.add_field(name = "Name:", value = member, inline = False)
        embed.add_field(name = "ID:", value = member.id, inline = False)
        embed.add_field(name = "Server:", value = member.guild, inline = False)
        embed.add_field(name = "Account Creation On:", value = member.created_at.strftime('%a %#d %B %Y, %I:%M %p UTC'), inline = False)
        embed.add_field(name = "Joined This Server On:", value = member.joined_at.strftime('%a %#d %B %Y, %I:%M %p UTC'), inline = False)
        embed.add_field(name = "Top Role:", value = member.top_role.mention, inline = False)
        embed.add_field(name = "Current Activity/Status:", value = member.activity, inline = False)
        embed.add_field(name = "Is A Bot?:", value = member.bot, inline = False)

        await ctx.send(embed = embed)


    # @commands.command(name='status', brief='Bot\'s Status', description='Get bot\'s status like ping, uptime etc.')
    # async def status(self, ctx):
    #     bot_ping = int(self.client.latency * 1000)
    #     bot_servers = len(self.client.guilds)
    #     current_time = time.time()
    #     difference = int(round(current_time - start_time))
    #     uptime = str(datetime.timedelta(seconds=difference))
    #     embed = discord.Embed(title = "Bot Status:", colour = self.client.user.colour)

    #     embed.set_thumbnail(url = self.client.user.avatar_url)

    #     embed.add_field(name = "Bot's Ping:", value = bot_ping, inline = False)
    #     embed.add_field(name = "Server Count:", value = bot_servers, inline = False)
    #     embed.add_field(name = "Bot's Uptime:", value = uptime, inline = False)

    #     await ctx.send(embed = embed)





    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if message.author == self.client.user:
                return


            mydb = mysql.connector.connect(
            host=config.sql_host,
            user=config.sql_user,
            password=config.sql_pass,
            database=config.sql_db
            )


            mycursor = mydb.cursor()

            user_exists = False

            mycursor.execute("SELECT * FROM user_data WHERE user_id='"+str(message.author.id)+"'")
            user_exists_check = mycursor.fetchall()
            for user_exists_data in user_exists_check:
                user_exists = True

            if user_exists == False:
                current_time_join = datetime.datetime.now()
                create_user_sql = "INSERT INTO user_data (user_id, username, money, locker, locker_limit, search, beg, pizza, apple, lucky_candy, bow, boar, hunt, server_vote, dbl_vote, topgg_vote, safenote) VALUES ('"+str(message.author.id)+"', '"+str(message.author).replace("'", "\\'")+"', 150, 0, 0, '2021-05-12 11:42:36.105276', '2021-05-12 11:42:36.105276', 0, 0, 0, 0, 0, '2021-05-12 11:42:36.105276', '2021-05-22 10:54:36', '2021-05-22 10:54:36', '2021-05-22 10:54:36', 0)"
                mycursor.execute(create_user_sql)
                mydb.commit()
            
            else:
                update_user_sql = "UPDATE `user_data` SET `username`='"+str(message.author).replace("'", "\\'")+"' WHERE user_id = '"+str(message.author.id)+"'"
                mycursor.execute(update_user_sql)
                mydb.commit()



            server_exists = False
            mycursor.execute("SELECT * FROM server_data WHERE server_id='"+str(message.guild.id)+"'")
            server_exists_check = mycursor.fetchall()
            for server_exists_data in server_exists_check:
                server_exists = True

            if server_exists == False:  
                # headers = {
                # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
                # }
                # send_mail_url = 'https://<mail sender api>&server='+message.guild.name
                # send_mail = requests.get(send_mail_url, headers=headers)
                create_server_sql = "INSERT INTO `server_data`(`server_id`, `server_name`, `members`, `text_channels`, `voice_channels`, `total_channels`) VALUES ('"+str(message.guild.id)+"','"+str(message.guild.name).replace("'", "\\'")+"','"+str(message.guild.member_count)+"','"+str(len(message.guild.text_channels))+"','"+str(len(message.guild.voice_channels))+"','"+str((len(message.guild.text_channels)+len(message.guild.voice_channels)))+"');"
                mycursor.execute(create_server_sql)
                mydb.commit()

            elif server_exists == True:
                update_server_sql= "UPDATE `server_data` SET `server_name`='"+str(message.guild.name).replace("'", "\\'")+"',`members`='"+str(message.guild.member_count)+"',`text_channels`='"+str(len(message.guild.text_channels))+"',`voice_channels`='"+str(len(message.guild.voice_channels))+"',`total_channels`='"+str((len(message.guild.text_channels)+len(message.guild.voice_channels)))+"' WHERE server_id='"+str(message.guild.id)+"'"
                mycursor.execute(update_server_sql)
                mydb.commit()

        except:
            pass
    


def setup(client):
    client.add_cog(Misc(client))