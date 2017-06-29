import discord
import asyncio
from discord.ext import commands
import subprocess
from subprocess import Popen
import bot_info

class Git:
    def __init__(self, client):
        self.client = client
    
    # Do git pull
    @commands.command(description='Runs "git pull" on the computer I\'m running on', pass_context=True)
    @bot_info.is_owner()
    async def pull(self):
        try:
            p = Popen(['git', 'pull'],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT)
                
            await ctx.send('Ran git pull!')
        except Exception as e:
            await ctx.send('Error:\n```\n' + str(e) + '```')
    
def setup(client):
    client.add_cog(Git(client))