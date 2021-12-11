import discord
import json
from wiktionaryparser import WiktionaryParser


class Client(discord.Client):

    def getWordData(message):
        req_content = message.content.split() #request content
        try:
            if len(req_content) >= 3:
                word = parser.fetch(req_content[1], req_content[2])
            else:
                word = parser.fetch(req_content[1])
            return word[0]
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

            help_mes.add_field(name="Pronounciation:", value=prefix+"pron <your word> (<language>)", inline=False)
            help_mes.add_field(name="Definition:", value=prefix+"def <your word> (<language>)", inline=False)
            help_mes.add_field(name="Examples:", value=prefix+"ex <your word> (<language> <max number of examples>)", inline=False)
            help_mes.add_field(name="Etymology:", value=prefix+"etym <your word> (<language>)", inline=False)
            help_mes.add_field(name="Change Prefix:", value=prefix+"prefix <new prefix>", inline=False)
            help_mes.add_field(name="Change Language:", value=prefix+"dlang <your preferred language in english>", inline=False)
            help_mes.add_field(name="*Please note!*", value="anything in parenthesis is optional, unless you're looking for a word in language different than default language (english).", inline=False)
            
            await message.channel.send(embed=help_mes)
            return

        # change defaul language
        elif message.content.startswith(prefix+'dlang'):
            new_lang = message.content.split()[1]
            # must check whether a valid language was chosen ######
            parser.set_default_language(new_lang)
            await message.channel.send('Default language has been been changed to '+parser.get_default_language())
            return

        # pronunciations
        elif message.content.startswith(prefix+'pron'):
            worddata = Client.getWordData(message)
            mes = discord.Embed(title = "Pronounciation(s) for \""+message.content.split()[1]+"\":", color = discord.Color.green())
            if worddata is None:
                mes.add_field(name="\u200b", value="*Could not find pronounciations for this word.*", inline=False)
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
            if worddata is None:
                mes.add_field(name="\u200b", value="*Could not find definitions for this word.*", inline=False)
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
            com = message.content.split()
            num = 3     # 3 examples as default
            if (len(com) == 4):
                try:
                    num = int(message.content.split()[3])   # number of examples
                except ValueError:
                    await message.channel.send("Invalid command")
                    return
            
            worddata = Client.getWordData(message)
            mes = discord.Embed(title = "Example(s) for \""+message.content.split()[1]+"\":", color = discord.Color.green())
            if worddata is None:
                mes.add_field(name="\u200b", value="*Could not find examples for this word.*", inline=False)
                await message.channel.send(embed=mes)
                return

            totalex = len(worddata['definitions'][0]['examples'])
            if (totalex < num):
                num = totalex

            text=""
            for i in range(num+1):
                text += (str(i)+". " if i!=0 else "")+worddata['definitions'][0]['examples'][i] + '\n\n'
            mes.add_field(name="\u200b", value=text, inline=False)
            await message.channel.send(embed=mes)

            return
        
        # etymology
        elif message.content.startswith(prefix+'etym'):     
            worddata = Client.getWordData(message)
            mes = discord.Embed(title = "Etymology for \""+message.content.split()[1]+"\":", color = discord.Color.green())
            if worddata is None:
                mes.add_field(name="\u200b", value="*Could not find etymology for this word.*", inline=False)
                await message.channel.send(embed=mes)
                return
            mes.add_field(name="\u200b", value=worddata['etymology'], inline=False)
            await message.channel.send(embed=mes)
            return

        # change prefix
        elif message.content.startswith(prefix+'prefix'):
            if (len(message.content.split()) != 2):
                await message.channel.send('Invalid command.\nType "'+prefix+'help" for available commands.')
                return
            newpre = message.content.split()[1]
            prefix = newpre

            await message.channel.send('Successfully changed prefix to \"'+newpre+'\"')
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
word_error_mes = " \nPlease make sure the word was written correctly.\nNote that default language is "+parser.get_default_language()

client = Client()
client.run(token)
