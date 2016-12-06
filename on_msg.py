import discord
import asyncio
import urllib.request
import subprocess
from subprocess import Popen
import json
import ec
import survey

ec_game = None
survey_inst = None

class Msger:
    def __init__(self, message, client):
        self.message = message
        self.client = client

    async def handle_msg(self):
        message = self.message
        client = self.client
        args = message.content.split()
        
        # Don't check the arguments if there are none
        if len(args) == 0:
            return
        
        # Test the bot
        if args[0] == '/ping':
            await client.send_message(message.channel, 'miaou !')
        
        bot_info = None
        with open('bot_info.json') as f:
            bot_info = json.load(f)
        # Do git pull
        if args[0] == '/pull' and message.author.id in bot_info['owners']:
            try:
                p = Popen(['git', 'pull'],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT)
                
                await client.send_message(message.channel, 'Ran git pull!')
            except Exception as e:
                await client.send_message(message.channel, 'Error:\n```\n' + str(e) + '```')

        # Change profile icon
        if args[0] == '/chg_avatar':
            try:
                # Read from URL
                if len(args) == 2:
                    a = urllib.request.urlopen(args[1]).read()
                    await client.edit_profile(avatar=a)
                    await client.send_message(message.channel, 'Avatar changed!')
                # Read from computer hosting the bot
                elif len(args) == 3 and args[1] == 'local':
                    with open(args[2], 'rb') as a:
                        await client.edit_profile(avatar=(a.read()))
                    await client.send_message(message.channel, 'Avatar changed!')
                # You didn't do it right
                else:
                    await client.send_message(message.channel, 'usage: /chg_avatar [local] url/file_path')
            except Exception as e:
                error_msg = 'Error:\n```\n' + str(e) + '\n```'
                await client.send_message(message.channel, error_msg)
        
        # Exquisite Corpse
        if args[0] == '/ec':
            global ec_game
            
            # End the game if it was finished
            if not ec_game is None and ec_game.killme == True:
                ec_game = None
                
            # Start the game if you gave 3 users
            if ec_game is None:
                players = message.mentions
                if len(players) == 3:
                    ec_game = ec.ECorpse(players[0], players[1], players[2])
                    await ec_game.welcome(message, client)
                else:
                    await client.send_message(message.channel, 'I want three players!')
            else:
                # End the game if it was started
                if len(args) == 2 and args[1] == 'end':
                    await client.send_message(message.channel, 'Game ended!')
                    ec_game = None
                # Allow people to input answers
                else:
                    await ec_game.input_answer(message, client, message.author)

        # Survey
        if args[0] == '/survey':
            try:
                global survey_inst
                
                if not survey_inst is None and not survey_inst.running:
                    survey_inst = None

                if survey_inst is None and len(args) > 1:
                    survey_inst = survey.Survey(message)
                    survey_inst = survey.prompt(message, client)
                elif len(args) == 1:
                    await client.send_message(message.channel, "I need a question first!")
                else:
                    if survey_inst.surveyor is message.author and len(args) > 1 and args[1] == '-end':
                        await survey_inst.end(message, client)
                        survey_inst = None
                    else:
                        await survey_inst.response(message, client)
            except Exception as e:
                err_msg = 'Err:\n```\n'
                err_msg += str(e) + '```'
                await client.send_message(message.channel, err_msg)

        # Clears the chat
        if args[0] == '/clear':
            await client.send_message(message.channel, '.' + '\n' * 100 + '.')

        # Removes your message (testing purposes)
        if args[0] == '/remove':
            await client.delete_message(message)
