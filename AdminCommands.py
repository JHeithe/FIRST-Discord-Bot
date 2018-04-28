import asyncio
import discord
from discord.ext import commands

class AdminCommands:
    bot = commands.Bot(command_prefix='&')

    def __init__(self, bot):
        self.bot = bot
    
    @bot.command(pass_context=True,description='Displays an ID')
    async def id(self, ctx, who:discord.Member):
        if AdminCommands.check_admin(ctx):
            await self.bot.say(who.name + "#" + str(who.discriminator) + ' has an id of: ' + str(who.id))
        else:
            msg = await self.bot.say('You do not have access to this command!')
            await asyncio.sleep(10)
            await self.bot.delete_message(msg)

    @commands.command(pass_context=True)
    async def purge(self, ctx, messagecount:int):
        if AdminCommands.check_admin(ctx):
            await self.bot.purge_from(ctx.message.channel,limit=messagecount+1)
            msg = await self.bot.say('Done!')
            await asyncio.sleep(10)
            await self.bot.delete_message(msg)
        else:
            msg = await self.bot.say('You do not have access to this command!')
            asyncio.sleep(10)
            await self.bot.delete_message(msg)

    @commands.command(pass_context=True,description='Sets nicknames, but it is meant for setting strictly my nickname yet it can be used to change anybodys nickname that I have access to.')
    async def nickset(self, ctx, member : discord.Member, nickname : str):
        if "@everyone" not in ctx.message.content and AdminCommands.check_admin(ctx):
            await self.bot.change_nickname(member,nickname)
            await self.bot.say(ctx.message.author.user + ', has changed ' + member.display_name + "'s nickname to: " + nickname)
        else:
            msg = await self.bot.say('You do not have access to this command!')
            await asyncio.sleep(10)
            await self.bot.delete_message(msg)

    @bot.command(pass_context=True)
    async def restart(self,ctx):
        if ctx.message.author.id in "166707716855693312":
            await self.bot.logout()
            #Create data dump to manage between restarts
        else:
            await self.bot.say('You do not have access to this command!')

    @commands.command(pass_context=True)
    async def serverlist(self,ctx):
        if AdminCommands.check_admin(ctx):
            server_list = ""
            for server in self.bot.servers:
                server_list += server.name + '\n'
            await self.bot.send_message(ctx.message.channel,server_list)
        else:
            await self.bot.send_message(ctx.message.channel,'You do not have access to this command!')

    @commands.command(pass_context=True)
    async def rolelist(self,ctx):
        if AdminCommands.check_admin(ctx):
            msg = await self.bot.send_message(ctx.message.channel,'Finding my roles...')
            my_roles = ''
            for role in msg.author.roles:
                if "@everyone" not in role.name:
                    my_roles += role.name + '\n'
            await self.bot.edit_message(msg,new_content='My roles are:\n'+my_roles)
        elif not found_admin:
            await self.bot.send_message(ctx.message.channel, 'You do not have access to this command!')

    @commands.command(pass_context=True)
    async def permissionlist(self,ctx):
        if AdminCommands.check_admin(ctx):
            msg = await self.bot.send_message(ctx.message.channel,'Finding my permissions...')
            my_permissions = ''
            for role in msg.author.roles:
                if role.permissions.create_instant_invite and "Create Instant Invite" not in my_permissions:
                    my_permissions += "Create Instant Invite\n"
                if role.permissions.kick_members and "Kick Members" not in my_permissions:
                    my_permissions += "Kick Members\n"
                if role.permissions.ban_members and "Ban Members" not in my_permissions:
                    my_permissions += "Ban Members\n"
                if role.permissions.administrator and "Administrator" not in my_permissions:
                    my_permissions += "Administrator\n"
                if role.permissions.manage_channels and "Manage Channels" not in my_permissions:
                    my_permissions += "Manage Channels\n"
                if role.permissions.manage_server and "Manage Server" not in my_permissions:
                    my_permissions += "Manage Server\n"
                if role.permissions.add_reactions and "Add Reactions" not in my_permissions:
                    my_permissions += "Add Reactions\n"
                if role.permissions.view_audit_logs and "View Audit Logs" not in my_permissions:
                    my_permissions += "View Audit Logs\n"
                if role.permissions.read_messages and "Read Messages" not in my_permissions:
                    my_permissions += "Read Messages\n"
                if role.permissions.send_messages and "Send Messages" not in my_permissions:
                    my_permissions += "Send Messages\n"
                if role.permissions.send_tts_messages and "Send TTS Messages" not in my_permissions:
                    my_permissions += "Send TTS Messages\n"
                if role.permissions.manage_messages and "Manage Messages" not in my_permissions:
                    my_permissions += "Manage Messages\n"
                if role.permissions.embed_links and "Embed Links" not in my_permissions:
                    my_permissions += "Embed Links\n"
                if role.permissions.attach_files and "Attach Files" not in my_permissions:
                    my_permissions += "Attach Files\n"
                if role.permissions.read_message_history and "Read Message History" not in my_permissions:
                    my_permissions += "Read Message History\n"
                if role.permissions.mention_everyone and "Mention Everyone" not in my_permissions:
                    my_permissions += "Mention Everyone\n"
                if role.permissions.external_emojis and "External Emojis" not in my_permissions:
                    my_permissions += "External Emojis\n"
                if role.permissions.connect and "Connect" not in my_permissions:
                    my_permissions += "Connect\n"
                if role.permissions.speak and "Speak" not in my_permissions:
                    my_permissions += "Speak\n"
                if role.permissions.mute_members and "Mute Members" not in my_permissions:
                    my_permissions += "Mute Members\n"
                if role.permissions.deafen_members and "Deafen Members" not in my_permissions:
                    my_permissions += "Deafen Members\n"
                if role.permissions.move_members and "Move Members" not in my_permissions:
                    my_permissions += "Move Members\n"
                if role.permissions.use_voice_activation and "Use Voice Activation" not in my_permissions:
                    my_permissions += "Use Voice Activation\n"
                if role.permissions.change_nickname and "Change Nickname" not in my_permissions:
                    my_permissions += "Change Nickname\n"
                if role.permissions.manage_nicknames and "Manage Nicknames" not in my_permissions:
                    my_permissions += "Manage Nicknames\n"
                if role.permissions.manage_roles and "Manage Roles" not in my_permissions:
                    my_permissions += "Manage Roles\n"
                if role.permissions.manage_webhooks and "Manage Webhooks" not in my_permissions:
                    my_permissions += "Manage Webhooks\n"
                if role.permissions.manage_emojis and "Manage Emojis" not in my_permissions:
                    my_permissions += "Manage Emojis\n"
            await self.bot.edit_message(msg,new_content='My permissions are:\n'+my_permissions)
        else:
            await self.bot.send_message(ctx.message.channel, 'You do not have access to this command!')
    
    @bot.command(pass_context=True)
    async def leaveserver(self,ctx):
        if ctx.message.author.id in "166707716855693312":
            for server in self.bot.servers:
                if server.name.lower() in ctx.message.content[len("&leaveserver "):].lower():
                    await self.bot.leave_server(server)
        else:
            await self.bot.say('You do not have acess to this command!')

    def check_message_yes(message):
        return message.content.lower().startswith('y')
    
    def check_admin(ctx):
        for role in ctx.message.author.roles:
            if ("admin" in role.name.lower() and "make first great again" in ctx.message.server.name.lower()) or ("moderator" in role.name.lower() and "first volunteers" in ctx.message.server.name.lower()) or ctx.message.author.id in "166707716855693312":
                return True
    
    def find_channel(self,server : discord.Server, name : str):
        for chnl in self.bot.get_all_channels():
            if name in chnl.name and chnl.server.id in server.id:
                return chnl
