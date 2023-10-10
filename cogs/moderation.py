import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions

class Moderation(commands.Cog):
    """be help Moderation"""

    def __init__(self, client):
        self.client = client

    @commands.command(name="serverinfo", brief="Gives Server Info", description="This command gives the server info such as name, number of users, text channels and voice channels.")
    async def serverinfo(self, ctx):
        c=0
        for member in ctx.guild.members:
            if member.bot:
                c = c + 1
                continue
        embed=discord.Embed(title="", description= "**Server id:** "+str(ctx.guild.id)+"\n**Server Name:** "+str(ctx.guild.name)+"\n**Total members:** "+str(ctx.guild.member_count)+"\n**Total Members excluding Bots:** "+str((ctx.guild.member_count - c))+"\n**Number of text channels:** "+str(len(ctx.guild.text_channels))+"\n**Number of voice channels:** "+str(len(ctx.guild.voice_channels)), color=discord.Color.blue())
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        await ctx.send(embed=embed)


    @commands.command(name="clear", brief="Delete Messages", description="This command can be used by users with manage messages permissions to delete messages in the server.", usage="<message number>")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amt=1):
        await ctx.message.delete()
        await ctx.channel.purge(limit=amt)
        if(amt == 1):
            await ctx.send(":white_check_mark: 1 message deleted!",  delete_after=1)
        else:
            await ctx.send(":white_check_mark: "+str(amt)+ " messages deleted!",  delete_after=1)

    @clear.error
    async def clear_error(self, ctx, error):
         for channel in ctx.guild.text_channels:
            if channel.permissions_for(ctx.author).manage_messages == False:
                await ctx.send("You do not have permissions to do that!")
            elif channel.permissions_for(ctx.guild.me).manage_messages == False:
                await channel.send('I do not have permissions to clear messages. You can give me the permission by enabling `Manage Messages` permission for my `BE Bot` role!')



    @commands.command(name="kick", brief="Kick user", description="Members with kick Member permissions can use this command to kick an user from a server", usage="<user> <reason (optional)>")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason = None):
        await member.kick(reason=reason)
        await ctx.send(f'Kicked {member.mention}')

    @kick.error
    async def kick_error(self, ctx, error):
        for channel in ctx.guild.text_channels:
            if channel.permissions_for(ctx.author).kick_members == False:
                await ctx.send("You do not have permissions to do that!")
            elif channel.permissions_for(ctx.guild.me).kick_members == False:
                await channel.send('I do not have permissions to kick an user. You can give me the permission by enabling `Kick Members` permission for my `BE Bot` role!')
            elif(ctx, MissingPermissions):
                embed=discord.Embed(title="The bot's role needs to be in a higher position, than the role the user to kick has in hierarchy.", color=discord.Color.red())
                embed.add_field(name="Need help?", value="https://imgur.com/a/y9Dvbu6", inline=False)
                await ctx.send(embed=embed)
            break



    @commands.command(name="ban", brief="Ban user", description="Members with Ban Member permissions can use this command to ban an user from a server", usage="<user> <reason (optional)>")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason = None):
        await member.ban(reason=reason)
        await ctx.send(f'Banned {member.mention}')

    @ban.error
    async def ban_error(self, ctx, error):
         for channel in ctx.guild.text_channels:
            if channel.permissions_for(ctx.author).ban_members == False:
                await ctx.send("You do not have permissions to do that!")
            elif channel.permissions_for(ctx.guild.me).ban_members == False:
                await channel.send('I do not have permissions to ban an user. You can give me the permission by enabling `Ban Members` permission for my `BE Bot` role!')
            elif(ctx, MissingPermissions):
                embed=discord.Embed(title="The bot's role needs to be in a higher position, than the role the user to ban has in hierarchy.", color=discord.Color.red())
                embed.add_field(name="Need help?", value="https://imgur.com/a/y9Dvbu6", inline=False)
                await ctx.send(embed=embed)
            break

    @commands.command(name="unban", brief="Unban user", description="Members with Ban Member permissions can use this command to unban an user in a server", usage="<user>")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
            if(user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.mention}')
                return

    @unban.error
    async def unban_error(self, ctx, error):
         for channel in ctx.guild.text_channels:
            if channel.permissions_for(ctx.author).ban_members == False:
                await ctx.send("You do not have permissions to do that!")
            elif channel.permissions_for(ctx.guild.me).ban_members == False:
                await channel.send('I do not have permissions to unban an user. You can give the permission to me by enabling `ban members` permission for my `BE Bot` role!')
            else:
                await ctx.send("Use mentioned was not found.")
            break


    # @commands.command(name="rr", brief="Unban user", description="Members with Ban Member permissions can use this command to unban an user in a server", usage="<user>")
    # async def rr(self, ctx, reaction, role: discord.Role, *, message):
    #     channel = bot.get_channel('')
    #     role = discord.utils.get(user.server.roles, name="CSGO_P")
    #     message = await bot.send_message(channel, "React to me!")
    #     reacted = await ct
    #     while True:
    #         reaction = await bot.wait_for_reaction(emoji="🏃", message=message)
    #         await bot.add_roles(reaction.message.author, role)
            


    


def setup(client):
    client.add_cog(Moderation(client))