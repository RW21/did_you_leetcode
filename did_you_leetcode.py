import asyncio
import os
import datetime
import discord
from dotenv import load_dotenv

# todo refactor


class Log:
    def __init__(self):
        self.channel = None
        self.date = datetime.date.today()
        self.members = {}
        self.write_to_file()

    def update_members(self, members):
        for member in members:
            if member not in self.members:
                self.members[member] = False

    def show_status(self):
        status_string = ''
        for member, done in self.members.items():
            if not done:
                status_string += str(member.name) + ' hasn\'t done Leetcode today\n'

        if not status_string:
            status_string = "Everyone has done Leetcode!"
        return status_string

    def write_to_file(self):
        f = open(str(self.date), "w+")
        f.close()

    def member_completed(self, member):
        if member in self.members:
            self.members[member] = True

    def finish_day(self):
        f = open(str(self.date), "w+")
        f.write()


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL = os.getenv('DISCORD_MAIN_CHANNEL')
main_channel = 'general'
client = discord.Client()
current_day = datetime.date.today()
current_log = Log()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    for guild in client.guilds:
        current_log.update_members([member for member in guild.members if not member.bot])

    print(current_log.members)


@client.event
async def on_message(message):
    current_log.update_members([member for member in message.guild.members if not member.bot])
    current_log.channel = message.channel

    if message.content.startswith('$done'):
        current_log.member_completed(message.author)
        await message.channel.send('Congrats!')

    if message.content.startswith('$status'):
        await message.channel.send(current_log.show_status())


async def my_background_task():
    await asyncio.sleep(5)
    await client.wait_until_ready()
    for ch in client.get_all_channels():
        print(ch)
        if ch.name == main_channel:
            channel = ch

    while not client.is_closed():
        # channel = list(client.get_all_channels())
        # channel = discord.utils.get(client.get_all_channels(), id=CHANNEL)
        print(channel)

        await channel.send(current_log.show_status())
        await asyncio.sleep(60 * 60)
        new_day = datetime.date.today()

        # todo refactor
        if current_day != new_day:
            current_day = new_day
            current_log = Log()
            for guild in client.guilds:
                current_log.update_members([member for member in guild.members if not member.bot])


client.loop.create_task(my_background_task())
client.run(TOKEN)
