import discord
from discord.ext import commands
from utils.message_format import MessageFormater


class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.message_formater = MessageFormater()
    @commands.command(name='kick')
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if member.guild_permissions.administrator:
            message = 'Aviv Hasdsay is the Admin, Bitch you cant kick me'
            formated_message = self.message_formater.get_block_quote_format(message)
            await ctx.send(formated_message)
            return
        message = f'Bot is kicking {member.display_name} from the server'
        formated_message = self.message_formater.get_block_quote_format(message)
        await ctx.send(formated_message)
        await member.kick(reason=reason)


    @commands.command(name='ban')
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member: discord.Member, *, reason: str=None):
        if member.guild_permissions.administrator:
            message = 'Aviv Hasdsay is the Admin, Bitch you cant ban me'
            formated_message = self.message_formater.get_block_quote_format(message)
            await ctx.send(formated_message)
            return
        message = f'Bot is banning {member.display_name} from the server'
        formated_message = self.message_formater.get_block_quote_format(message)
        await ctx.send(formated_message)
        await member.ban(reason=reason)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unban(self,ctx, *, member: discord.Member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.channel.send(f"Unbanned: {user.mention}")


    async def cog_command_error(self, ctx, error):
        if isinstance(error, error.MissingPermissions):
            await ctx.send("You don't have the right permission for this command!")

def setup(bot):
    bot.add_cog(Admin(bot))