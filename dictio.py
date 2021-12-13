import discord
import json
from wiktionaryparser import WiktionaryParser
from textblob import TextBlob


class Client(discord.Client):

    def getWordData(message):
        if len(message.content.split()) > 3:
            return None
        
        word = message.content.split()[1]
        
        try:
            lang_code = TextBlob(word).detect_language()
            config_file = open('language.json',)
            data = json.load(config_file)
            lang = data[lang_code].lower()
            config_file.close()
        except OSError:
            print ("Could not open/read file: language.json")
            return None
        
        try:
            worddata = parser.fetch(word, lang)
            return worddata[0]
        except:
            return None

    async def on_ready(self):
        print('Logged in as {0}'.format(self.user))

    async def on_message(self, message):
        if message.author == self.user:
            return
        global prefix
        if not message.content.startswith(prefix):
            return

        # help
        if message.content.startswith(prefix+'help'):
            help_mes = discord.Embed(title = "Available Commands", color = discord.Color.green())

            help_mes.add_field(name="Pronounciation:", value=prefix+"pron <your word>", inline=False)
            help_mes.add_field(name="Definition:", value=prefix+"def <your word>", inline=False)
            help_mes.add_field(name="Examples:", value=prefix+"ex <your word> (<max number of examples>)", inline=False)
            help_mes.add_field(name="Etymology:", value=prefix+"etym <your word>", inline=False)
            help_mes.add_field(name="Change Prefix:", value=prefix+"prefix <new prefix>", inline=False)
            help_mes.add_field(name="*Please note!*", value="anything in parenthesis is optional", inline=False)
            
            await message.channel.send(embed=help_mes)
            return

        # pronunciations
        elif message.content.startswith(prefix+'pron'):
            worddata = Client.getWordData(message)
            mes = discord.Embed(title = "Pronounciation(s) for \""+message.content.split()[1]+"\":", color = discord.Color.green())

            if (len(message.content.split()) != 2):
                mes.add_field(name="\u200b", value="*Not a valid command.\n\nType {:s}help for list of available commands.*".format(prefix), inline=False)
                await message.channel.send(embed=mes)
                return

            if worddata is None:
                mes.add_field(name="\u200b", value="*Could not find pronounciations for this word.\nPlease check your spelling, and command format.\n\nType {:s}help for list of available commands.*".format(prefix), inline=False)
                await message.channel.send(embed=mes)
                return

            text=""
            for i in range(len(worddata)):
                text += worddata['pronunciations']['text'][i] + '\n\n'
            mes.add_field(name="\u200b", value=text, inline=False)
            await message.channel.send(embed=mes)
            return
            
        # definitions
        elif message.content.startswith(prefix+'def'):
            worddata = Client.getWordData(message)
            mes = discord.Embed(title = "Definition(s) for \""+message.content.split()[1]+"\":", color = discord.Color.green())
            
            if (len(message.content.split()) != 2):
                mes.add_field(name="\u200b", value="*Not a valid command.\n\nType {:s}help for list of available commands.*".format(prefix), inline=False)
                await message.channel.send(embed=mes)
                return

            if worddata is None:
                mes.add_field(name="\u200b", value="*Could not find definitions for this word.\nPlease check your spelling, and command format.\n\nType {:s}help for list of available commands.*".format(prefix), inline=False)
                await message.channel.send(embed=mes)
                return
            text=""
            for i in range(len(worddata)):
                text += (str(i)+". " if i!=0 else "")+worddata['definitions'][0]['text'][i] + '\n\n'
            mes.add_field(name="\u200b", value=text, inline=False)
            await message.channel.send(embed=mes)
            return

        # examples
        elif message.content.startswith(prefix+'ex'):
            mes = discord.Embed(title = "Example(s) for \""+message.content.split()[1]+"\":", color = discord.Color.green())
            
            num = 4     # 3 examples as default
            if (len(message.content.split()) == 3):
                try:
                    num = int(message.content.split()[2])   # number of examples
                except ValueError:
                    mes.add_field(name="\u200b", value="*Not a valid command.\n\nType {:s}help for list of available commands.*".format(prefix), inline=False)
                    await message.channel.send(embed=mes)
                    return
            
            worddata = Client.getWordData(message)
            if worddata is None:
                mes.add_field(name="\u200b", value="*Could not find examples for this word.\nPlease check your spelling, and command format.\n\nType {:s}help for list of available commands.*".format(prefix), inline=False)
                await message.channel.send(embed=mes)
                return

            totalex = len(worddata['definitions'][0]['examples'])
            if (totalex < num):
                num = totalex
            
            text=""
            for i in range(num):
                text += (str(i)+". " if i!=0 else "")+worddata['definitions'][0]['examples'][i] + '\n\n'
            mes.add_field(name="\u200b", value=text, inline=False)
            await message.channel.send(embed=mes)

            return
        
        # etymology
        elif message.content.startswith(prefix+'etym'):     
            worddata = Client.getWordData(message)
            mes = discord.Embed(title = "Etymology for \""+message.content.split()[1]+"\":", color = discord.Color.green())
            
            if (len(message.content.split()) != 2):
                mes.add_field(name="\u200b", value="*Not a valid command.\n\nType {:s}help for list of available commands.*".format(prefix), inline=False)
                await message.channel.send(embed=mes)
                return

            if worddata is None:
                mes.add_field(name="\u200b", value="*Could not find etymology for this word.\nPlease check your spelling, and command format.\n\nType {:s}help for list of available commands.*".format(prefix), inline=False)
                await message.channel.send(embed=mes)
                return
            mes.add_field(name="\u200b", value=worddata['etymology'], inline=False)
            await message.channel.send(embed=mes)
            return

        # change prefix
        elif message.content.startswith(prefix+'prefix'):
            mes = discord.Embed(title = "Changing prefix...", color = discord.Color.green())
            
            if (len(message.content.split()) != 2):
                mes.add_field(name="\u200b", value="*Not a valid command.\n\nType {:s}help for list of available commands.*".format(prefix), inline=False)
                await message.channel.send(embed=mes)
                return

            newpre = message.content.split()[1]
            prefix = newpre

            mes.add_field(name="\u200b", value="Successfully changed prefix to \""+newpre+"\"".format(prefix), inline=False)
            await message.channel.send(embed=mes)
            return
            
        if message.content[2::] == 'ping':
            await message.channel.send('pong')
            return
        if message.content[2::] in hello_mes_list:
            await message.channel.send("hello! :)")
            return

        await message.channel.send('Invalid command, type '+prefix+'help for list of available commands.')


config_file = open('config.json',)
data = json.load(config_file)

token = data['token']
prefix = data['prefix']
config_file.close()

parser = WiktionaryParser()

hello_mes_list = ['hello! :)', 'hi', 'hi!', 'hello', 'hello!', 'hey', 'hey!']

client = Client()
client.run(token)
