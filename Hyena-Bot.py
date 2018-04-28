import os
import discord
from discord.ext import commands
import time
import asyncio
import platform
import requests
import json

from AdminCommands import AdminCommands

# Setup Nameless
path = os.path.realpath('')
operating_system = platform.platform()
all_contents = ''
if "Windows" in operating_system:
    f = open(path + '\\token.txt','r')
    all_contents = f.read()
else:
    f = open(path + '/token.txt','r')
    all_contents = f.read()

tba_token = ""
if "Windows" in operating_system:
    f = open(path + '\\tbatoken.txt','r')
    tba_token = f.read()
    tba_token = tba_token[:len(tba_token)-1]
else:
    f = open(path + '/tbatoken.txt','r')
    tba_token = f.read()
    tba_token = tba_token[:len(tba_token)-1]

# FOR DISCORD
bot = commands.Bot(command_prefix='*', description='')
bot.remove_command('help')
afk_statuses = []
questions = {}


@bot.event
async def on_ready():
    bot.add_cog(AdminCommands(bot))
    print('Running version number: ' + discord.__version__)
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-----------------')
    await bot.change_presence(game=discord.Game(name='&help'))


@bot.event
async def on_message(message):
    if len(message.mentions) > 0:
        for mention in message.mentions:
            if mention.id == bot.user.id and not message.author.bot:
                if "what is your purpose?" in message.content.lower():
                    await bot.send_message(message.channel, 'To pass butter.')
                elif "what is your prefix?" in message.content.lower() or "what's your prefix?" in message.content.lower():
                    await bot.send_message(message.channel, 'My prefix is `*` please use it sparingly.')
                elif "what is the meaning of life?" in message.content.lower():
                    await bot.send_message(message.channel, '42.')
            for afkstatus in afk_statuses:
                if afkstatus[0].id in mention.id:
                    embed = discord.Embed()
                    embed.title = afkstatus[0].display_name + ' is afk'
                    embed.description = afkstatus[1]
                    embed.set_footer(text='Triggered by: ' + message.author.display_name,icon_url=afkstatus[0].avatar_url)
                    message_response = await bot.send_message(message.channel,embed=embed)
                    await asyncio.sleep(10)
                    await bot.delete_message(message_response)
                elif afkstatus[0].id in message.author.id:
                    afk_statuses.remove(afkstatus)
                    afk_response = await bot.send_message(message.channel, message.author.display_name + ' is no longer afk.')
                    await asyncio.sleep(10)
                    await bot.delete_message(afk_response)
    else:
        if message.content.lower().startswith('(☞ﾟヮﾟ)☞') and not message.author.bot:
            await bot.send_message(message.channel,'☜(ﾟヮﾟ☜)')
        elif message.content.startswith('☜(ﾟヮﾟ☜)') and not message.author.bot:
            await bot.send_message(message.channel,'(☞ﾟヮﾟ)☞')
        for afkstatus in afk_statuses:
            if afkstatus[0].id in message.author.id:
                afk_statuses.remove(afkstatus)
                afk_response = await bot.send_message(message.channel,message.author.display_name + ' is no longer afk.')
                await asyncio.sleep(10)
                await bot.delete_message(afk_response)
    await bot.process_commands(message)


@bot.event
async def on_voice_state_update(before,after):
    if "austin's sarcastic server" in after.server.name.lower():
        for role in before.roles:
            if "voice-general" in role.name.lower():
                await bot.remove_roles(before,role)
        for role in after.server.roles:
            if after.voice.voice_channel.name.lower().replace(" ", "-").replace("(", "").replace(")", "") in role.name.lower():
                await bot.add_roles(after,role)


##################################################
#                 Help Command                   #
##################################################

user_commands = {"nick":{"title":"nick", "description":"Command used to change your nickname", "usage":"Example: &nick [nickname]"},
"ping":{"title":"ping", "description":"Used to check latency between the bot and the Discord API", "usage":"Example: &ping"},
"afk":{"title":"afk", "description":"Used to note that you are away from keyboard.", "usage":"Example: &afk [reason]"},
"hug":{"title":"hug", "description":"Gives people hugs", "usage":"Example: &hug [mention]"},
"invite":{"title":"invite", "description":"Invite link to bring Nameless to your server", "usage":"Example: &invite"},
"giveme":{"title":"giveme", "description":"Give yourself roles", "usage":"Example: &giveme [role name]"},
"removeme":{"title":"removeme", "description":"Remove your own roles", "usage":"Example: &removeme [role name]"},
"tba":{"title":"tba", "description":"Check stats about FIRST Robotics Competition teams", "usage":"Example: &tba [search_type] [team_number]"},
"whohas":{"title":"whohas", "description":"Command to check who has a role or nickname", "usage":"Example: &whohas [search_type] [search]"}}
admin_commands = {"id":{"title":"id", "description":"Check user's id", "usage":"Example: &id [mention]"}, "purge":{"title":"purge", "description":"Used to delete more than one message in a channel", "usage":"Example: &purge [messages_to_purge]"}, "nickset":{"title":"nickset", "description":"Forced setting of someone else's nickname", "usage":"Example: &nickset [mention] [change_to]"}}
host_commands = {"restart":{"title":"restart", "description":"Restarts Nameless and pulls a new github version", "usage":"Example: &restart"}, "leaveserver":{"title":"leaveserver", "description":"Can be used to tell the bot to leave a server", "usage":"Example: &leaveserver"}}

@bot.command(pass_context=True)
async def help(ctx):
    # Get a count of how many commands are available
    count = len(user_commands)
    
    embed = discord.Embed()
    embed.title = "Help Menu "
    if len(ctx.message.content) > len("&help "):
        embed.add_field(name=ctx.message.content[len("&help "):],value="test", inline=False)
        embed.set_author(ctx.message.author,icon_url=ctx.message.author.avatar_url)
    else:
        is_host = False
        if ctx.message.author.id in "242090372115726337":
            is_host = True
        for command in user_commands:
            embed.add_field(name=user_commands[command]["title"], value=user_commands[command]["description"], inline=False)
        is_admin = False
        for role in ctx.message.author.roles:
            if role.permissions.administrator:
                is_admin = True
        if is_admin or is_host:
            count += len(admin_commands)
            for command in admin_commands:
                embed.add_field(name=admin_commands[command]["title"], value=admin_commands[command]["description"], inline=False)
        if is_host:
            count += len(host_commands)
            for command in host_commands:
                embed.add_field(name=host_commands[command]["title"], value=host_commands[command]["description"], inline=False)
        embed.title += "(" + str(count) + "):"
    await bot.say(embed=embed)


##################################################
#             Standard bot commands              #
##################################################


@bot.command(pass_context=True,description='Changes a Members nickname')
async def nick(ctx):
    nick_length = len("&nick ")
    if len(ctx.message.content) == nick_length-1 or len(ctx.message.content) == nick_length:
        await bot.say("To use &nick, please specify `&nick ` followed by the nickname you would like to have. Maximum of 32 characters.")
    elif len(ctx.message.content) > (nick_length + 32):
        await bot.say("Nickname unusable, please limit the nickname to 32 characters. (Cut off: " + ctx.message.content[nick_length+32:] + ")")
    else:
        await bot.change_nickname(ctx.message.author,ctx.message.content[nick_length:])
        await bot.say("Nickname changed! " + ctx.message.author.mention)


@bot.command(pass_context=True,description='Test the latency between your server and me')
async def ping(ctx):
    pingtime = time.time()
    pingms = await bot.say('Pinging...')
    ping = (time.time() - pingtime)*1000
    await bot.edit_message(pingms, 'Pong! Time taken is: ' + str(ping)[:str(ping).index(".")] + ' milliseconds')


@bot.command(pass_context=True)
async def afk(ctx):
    afk_statuses.append([ctx.message.author, ctx.message.content[len('&afk '):]])
    embed = discord.Embed()
    embed.title = ctx.message.author.display_name + ' is now afk'
    embed.description = ctx.message.content[len('& afk'):]
    embed.set_footer(text='Triggered_by: ' + ctx.message.author.display_name,icon_url=ctx.message.author.avatar_url)
    afk_message = await bot.say(embed=embed)
    await asyncio.sleep(5)
    await bot.delete_message(afk_message)

@bot.command(pass_context=True)
async def hug(ctx):
    if len(ctx.message.content) < len("&hug ") or len(ctx.message.mentions) < 1:
        await bot.say("*hugs* " + ctx.author.display_name)
    else:
        await bot.say("*hugs* " + ctx.message.mentions[0].display_name)

@bot.command()
async def invite(self):
    await self.bot.say("Invite me to your server!\nhttps://discordapp.com/oauth2/authorize?client_id=" + str(self.bot.user.id) + "&scope=bot")

@bot.command(pass_context=True)
async def giveme(ctx):
    roleName = ctx.message.content[len('&giveme '):]
    
    # Create non-accessible giveme roles
    not_accessible_roles = []
    if "Windows" in operating_system:
        f = open(path + '\\roles.txt','r')
        not_accessible_roles = f.read().split("\n")
    else:
        f = open(path + '/roles.txt','r')
        not_accessible_roles = f.read().split("\n")
    
    ## Complete giveme command
    if len(ctx.message.content) == 7 or "list" in roleName.lower():
        await bot.say('Currently available roles:')
        toSend = ""
        for role in ctx.message.server.roles:
            if role.name.lower() not in not_accessible_roles:
                toSend += role.name + "\n"
        if len(toSend) > 5:
            await bot.say(toSend)
        else:
            await bot.say("Could not find any available roles.")
    else:
        role_found = False
        for role in ctx.message.server.roles:
            if roleName.lower() in role.name.lower() and roleName.lower() not in not_accessible_roles:
                await bot.add_roles(ctx.message.author, role)
                await bot.say('Successfully added ' + role.name + ' to ' + ctx.message.author.mention)
                role_found = True
        if not role_found:
            await bot.say('You cannot add that role to yourself because it either does not exist or because you do not have access to it.')


@bot.command(pass_context=True)
async def removeme(ctx, roleName:str):
    accessible = True
    
    # Create non-accessible removeme roles
    not_accessible_roles = []
    if "Windows" in operating_system:
        f = open(path + '\\roles.txt','r')
        not_accessible_roles = f.read().split("\n")
    else:
        f = open(path + '/roles.txt','r')
        not_accessible_roles = f.read().split("\n")
    
    if roleName.lower() not in not_accessible_roles:
        for role in ctx.message.author.roles:
            if roleName.lower() in role.name.lower() and (len(roleName) - 2 < len(role.name) or len(roleName) + 2 > len(role.name)) and "admin" not in role.name.lower() and "moderator" not in role.name.lower() and "advisor" not in role.name.lower():
                await bot.remove_roles(ctx.message.author, role)
                await bot.say('Successfully removed ' + role.name + ' from ' + ctx.message.author.mention)
    else:
        await bot.say('You do not have access to that nickname here.')


@bot.command(pass_context=True)
async def tba(ctx):
    if len(ctx.message.content.replace(" ", "")[len('&tba '):]) < 2:
        tba_example = discord.Embed(title='&tba Command Example')
        tba_example.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)
        tba_example.description = '&tba [search_type] [team number]\n\n' + 'Available search types:\n' + '   team, divison, events, teamname'
        tba_example.color = discord.Color.blue()
        tba_example.set_thumbnail(url="https://www.thebluealliance.com/images/logo_square_512.png")
        await bot.say(embed=tba_example)
    else:
        content = ctx.message.content.lower().split(" ")
        tba_embed = discord.Embed(title="The Blue Alliance")
        if "division" in ctx.message.content.lower().split(" ")[1]:
            division_keys = ["2018carv", "2018gal", "2018hop", "2018new", "2018roe", "2018tur", "2018arc", "2018cars", "2018cur", "2018dal", "2018dar", "2018tes"]
            division_convert = {"2018carv":"Carver", "2018gal":"Galileo", "2018hop":"Hopper", "2018new":"Newton", "2018roe":"Roebling", "2018tur":"Turing", "2018arc":"Archimedes", "2018cars":"Carson", "2018cur":"Curie", "2018dal":"Daly", "2018dar":"Darwin", "2018tes":"Tesla"}
            division_keys_text = []
            found = False
            for division in division_keys:
                division_keys_text += [requests.get("https://www.thebluealliance.com/api/v3/event/" + division + "/teams", headers={"X-TBA-Auth-Key":tba_token}).text]
                for entry in json.loads(division_keys_text[len(division_keys_text)-1]):
                    if int(entry["team_number"]) == int(ctx.message.content.split(" ")[2]):
                        tba_embed.add_field(name="Team:", value=str(entry["team_number"]) + " - " + entry["nickname"],inline=False)
                        tba_embed.add_field(name="Division:",value=division_convert[division],inline=False)
                        found = True
                        break
                if found:
                    break
            if len(tba_embed.fields) < 1:
                text = requests.get("https://www.thebluealliance.com/api/v3/team/frc" + ctx.message.content.lower().split(" ")[2], headers={"X-TBA-Auth-Key":tba_token}).text
                data = json.loads(text)
                tba_embed.add_field(name="Team:", value=ctx.message.content.lower().split(" ")[2] + " - " + data["nickname"],inline=False)
                tba_embed.add_field(name="Division:", value="Not found! This team is not in a division.",inline=False)
        elif "team" in ctx.message.content.lower().split(" ")[1] and len(ctx.message.content.lower().split(" ")[1]) == 4:
            text = requests.get("https://www.thebluealliance.com/api/v3/team/frc" + ctx.message.content.lower().split(" ")[2], headers={"X-TBA-Auth-Key":tba_token}).text
            data = json.loads(text)
            tba_embed.add_field(name="Team:", value=ctx.message.content.lower().split(" ")[2] + " - " + data["nickname"], inline=False)
            tba_embed.add_field(name="Location:",value=data["city"] + ", " + data["state_prov"] + ", " + data["country"] + " " + data["postal_code"],inline=False)
            tba_embed.add_field(name="Motto:",value=data["motto"],inline=False)
        elif "event" in ctx.message.content.lower().split(" ")[1]:
            text = requests.get("https://www.thebluealliance.com/api/v3/team/frc" + ctx.message.content.lower().split(" ")[2] + "/events/2018", headers={"X-TBA-Auth-Key":tba_token}).text
            data = json.loads(text)
            tba_embed.add_field(name="Team Number:", value=ctx.message.content.lower().split(" ")[2],inline=False)
            events = ""
            for event_data in data:
                events += str(event_data["name"]) + ", "
            if len(events) > 2:
                events = events[:len(events)-2]
            tba_embed.add_field(name="Events:",value=events,inline=False)
        elif "teamname" in ctx.message.content.lower().split(" ")[1]:
            found_team_numbers = []
            search_content = ""
            for content in ctx.message.content.split(" "):
                if "&tba" not in content.lower() and "teamname" not in content.lower():
                    search_content += content + " "
            search_content = search_content[:len(search_content)-1]
            for i in range(15):
                text = requests.get("https://www.thebluealliance.com/api/v3/teams/" + str(i) + "/simple",headers={"X-TBA-Auth-Key":tba_token}).text
                data = json.loads(text)
                for team in data:
                    if search_content.lower() in team["nickname"].lower():
                        found_team_numbers += [team["team_number"]]
            discovered_teams = ""
            for i in found_team_numbers:
                discovered_teams += str(i) + "\n"
            if len(discovered_teams) > 0:
                tba_embed.add_field(name="Teams found with " + search_content + ":", value=str(discovered_teams))
        tba_embed.color = discord.Color.blue()
        tba_embed.set_thumbnail(url="https://www.thebluealliance.com/images/logo_square_512.png")
        await bot.say(embed=tba_embed)


@bot.command(pass_context=True)
async def whohas(ctx):
    if len(ctx.message.content[len('&whohas'):]) < 2:
        whohas_example = discord.Embed(title='&whohas')
        whohas_example.set_footer(text='Triggered by: ' + ctx.message.author.display_name,icon_url=ctx.message.author.avatar_url)
        whohas_example.description = '&whohas [search_type] [search content]\n' + 'Available search types:\n' + '   role, nick'
        await bot.say(embed=whohas_example)
    else:
        name = ctx.message.content[len('&whohas nick '):]
        people_with_name = ''
        for member in ctx.message.server.members:
            if ctx.message.content.lower().startswith('&whohas nick '):
                if ctx.message.content[len('&whohas nick '):].lower() in member.display_name.lower():
                    people_with_name += member.display_name + '\n'
            elif ctx.message.content.lower().startswith('&whohas role '):
                for role in member.roles:
                    if role.name.lower().startswith(name.lower()):
                        people_with_name += member.display_name + '\n'
        total_users = len(people_with_name.split('\n'))-1
        messages = partition_message(people_with_name)
        i = 0
        if len(messages) < 15:
            sent_messages = []
            while i < len(messages):
                embed = whohas_partition(ctx.message.author, name, total_users)
                if len(messages) - 3 >= i:
                    embed.add_field(name='['+str(i+1)+'/'+str(len(messages))+']',value=messages[i],inline=True)
                    embed.add_field(name='['+str(i+2)+'/'+str(len(messages))+']',value=messages[i+1],inline=True)
                    embed.add_field(name='['+str(i+3)+'/'+str(len(messages))+']',value=messages[i+2],inline=True)
                    i += 3
                elif len(messages) - 2 >= i:
                    embed.add_field(name='['+str(i+1)+'/'+str(len(messages))+']',value=messages[i],inline=True)
                    embed.add_field(name='['+str(i+2)+'/'+str(len(messages))+']',value=messages[i+1],inline=True)
                    i += 2
                else:
                    embed.add_field(name='['+str(i+1)+'/'+str(len(messages))+']',value=messages[i],inline=True)
                    i+=1
                sent_messages.append(await bot.say(embed=embed))
            await asyncio.sleep(10)
            await bot.purge_from(ctx.message.channel, limit=len(sent_messages))
        else:
            embed = whohas_partition(ctx.message.author, name, total_users)
            embed.add_field(name='[1/1]',value='There are too many users with this role or nickname.')
            await bot.say(embed=embed)
            await asyncio.sleep(10)
            await bot.purge_from(ctx.message.channel, limit=1)


def whohas_partition(author : discord.Member, name : str, total_users : int):
    whohas_embed = discord.Embed()
    whohas_embed.title = 'Users with ' + name + ':'
    whohas_embed.set_footer(text='Triggered by:' + author.display_name + ' | User Count: ' + str(total_users),icon_url=author.avatar_url)
    return whohas_embed


def partition_message(message : str):
    partitions = []
    for part in message.split('\n'):
        if len(partitions) == 0:
            partitions += [part + '\n']
        elif len(partitions[len(partitions)-1] + '\n' + part) > 1000:
            partitions += [part + '\n']
        else:
            partitions[len(partitions)-1] += part + '\n'
    return partitions


def find_channel(server : discord.Server, name : str):
    for chnl in bot.get_all_channels():
        if name in chnl.name and chnl.server.id in server.id:
            return chnl


# Start Nameless
bot.run(all_contents[:len(all_contents)-1])
