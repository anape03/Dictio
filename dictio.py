import discord
import json
from wiktionaryparser import WiktionaryParser


def printData(all_data, title=''):
        text = title+':\n'
        for i in range(len(all_data)):
            text += all_data[i] + '\n'
        return text

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
        if not message.content.startswith(prefix):
            return

        # help
        if message.content.startswith(prefix+'help'):
            await message.channel.send('Available commands: \n\
Pronounciation:\n\t'+prefix+'pron <your word> (<language>)\n\
Definition:\n\t'+prefix+'def <your word> (<language>)\n\
Examples:\n\t'+prefix+'ex <your word> (<language> <max number of examples>)\n\
Etymology:\n\t'+prefix+'etym <your word> (<language>)\n\
\nPlease note: anything in parenthesis is optional, unless you\'re looking\n\
for a word in language different than default language ('+parser.get_default_language()+').\n\
You may change the default language using the command: \n\
'+prefix+'dlang <your preferred language in english>')
            return

        # change defaul language
        elif message.content.startswith(prefix+'dlang'):
            new_lang = message.content.split()[1]
            # must check weather a valid language was chosen
            parser.set_default_language(new_lang)
            await message.channel.send('Default language has been been changed to '+parser.get_default_language())
            return

        # pronunciations
        elif message.content.startswith(prefix+'pron'):
            worddata = Client.getWordData(message)
            if worddata is None:
                await message.channel.send('Could not find pronounciation for this word.'+error_mes)
                return
            await message.channel.send(printData(worddata['pronunciations']['text'], 'Pronunciation(s)'))
            return
            
        # definitions
        elif message.content.startswith(prefix+'def'):
            worddata = Client.getWordData(message)
            if worddata is None:
                await message.channel.send('Could not find definition for this word.'+error_mes)
                return
            await message.channel.send(printData(worddata['definitions'][0]['text'], 'Definition(s)'))
            return

        # examples
        elif message.content.startswith(prefix+'ex'):
            com = [message.content.split()]
            if (len(com) == 4):
                try:
                    num = int(message.content.split()[3]) #number of examples
                except ValueError:
                    await message.channel.send("Invalid command")
                    return
            worddata = Client.getWordData(message)
            if worddata is None:
                await message.channel.send('Could not find examples for this word.'+error_mes)
                return
            await message.channel.send(printData(worddata['definitions'][0]['examples'][:3:], 'Examples'))
            return
        
        # etymology
        elif message.content.startswith(prefix+'etym'):     
            worddata = Client.getWordData(message)
            if worddata is None:
                await message.channel.send('Could not find etymology for this word.'+error_mes)
                return
            print(type(worddata['etymology']))
            await message.channel.send('Etymology:\n'+worddata['etymology'])
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
error_mes = " \nPlease make sure the word was written correctly.\nNote that default language is "+parser.get_default_language()

client = Client()
client.run(token)
