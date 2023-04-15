import discord
from discord.ext import commands
from dotenv import load_dotenv
import re
import enchant
import os

en = enchant.Dict("en_US")
ru = enchant.Dict("ru_RU")

# LOADS THE .ENV FILE THAT RESIDES ON THE SAME LEVEL AS THE SCRIPT.
load_dotenv()

# THE API TOKEN
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.reactions = True
client = commands.Bot(command_prefix='/', intents=intents)

help_command_description = "/help - get all included commands"
ping_command_description = "/ping - check bot status"
convert_command_description = "/convert - converting replied text to russian/english language"

emoji = '\N{THUMBS UP SIGN}'
english_to_russian = {
    'q': 'й', 'w': 'ц', 'e': 'у', 'r': 'к', 't': 'е', 'y': 'н', 'u': 'г', 'i': 'ш', 'o': 'щ', 'p': 'з', '[': 'х', ']': 'ъ', 'a': 'ф', 's': 'ы', 'd': 'в', 'f': 'а', 'g': 'п', 'h': 'р', 'j': 'о', 'k': 'л', 'l': 'д', ';': 'ж', "'": 'э', 'z': 'я', 'x': 'ч', 'c': 'с', 'v': 'м', 'b': 'и', 'n': 'т', 'm': 'ь', ',': 'б', '.': 'ю', '/': '.',
    'Q': 'Й', 'W': 'Ц', 'E': 'У', 'R': 'К', 'T': 'Е', 'Y': 'Н', 'U': 'Г', 'I': 'Ш', 'O': 'Щ', 'P': 'З', '{': 'Х', '}': 'Ъ', 'A': 'Ф', 'S': 'Ы', 'D': 'В', 'F': 'А', 'G': 'П', 'H': 'Р', 'J': 'О', 'K': 'Л', 'L': 'Д', ':': 'Ж', '"': 'Э', 'Z': 'Я', 'X': 'Ч', 'C': 'С', 'V': 'М', 'B': 'И', 'N': 'Т', 'M': 'Ь', '<': 'Б', '>': 'Ю', '?': ','
}
russian_to_english = {v: k for k, v in english_to_russian.items()}


def switch_keyboard_layout(text, layout_mapping):
    return ''.join([layout_mapping.get(char, char) for char in text])


@client.event
async def on_ready():
    guild_count = 0

    for guild in client.guilds:
        print(f"- {guild.id} (name: {guild.name})")
        guild_count = guild_count + 1

    print("KeyLayoutFixer is in " + str(guild_count) + " guilds.")


@client.command()
async def ping(ctx):
    await ctx.send('Pong')


@client.command()
async def convert(ctx):
    if ctx.message.reference is not None:
        # Get the replied message
        replied_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)

        await ctx.message.add_reaction(emoji)

        # Try converting with both layouts and pick the one with more English characters
        eng_converted = switch_keyboard_layout(
            replied_message.content, russian_to_english)
        rus_converted = switch_keyboard_layout(
            replied_message.content, english_to_russian)

        if eng_converted == replied_message.content:
            await ctx.send(rus_converted)
        else:
            await ctx.send(eng_converted)

    else:
        await ctx.send("Please reply to a message with the !convert command to convert the text.")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    message_without_mention = delete_mention(message.content)

    eng_converted = switch_keyboard_layout(
        message_without_mention, russian_to_english)
    rus_converted = switch_keyboard_layout(
        message_without_mention, english_to_russian)
        
    separated_eng_message = checking_list_for_empty_str(separate_message(eng_converted))
    separated_rus_message = checking_list_for_empty_str(separate_message(rus_converted))

    if separated_eng_message and separated_rus_message:
        rus_words_checked = checking_for_words(separated_rus_message)
        eng_words_checked = checking_for_words(separated_eng_message)

        if eng_words_checked > rus_words_checked:
            if message_without_mention != eng_converted:
                await message.channel.send(eng_converted)
        elif eng_words_checked < rus_words_checked:
            if message_without_mention != rus_converted:
                await message.channel.send(rus_converted)

    await client.process_commands(message)

def delete_mention(message):
    return re.sub(r'<@!?(\d+)>|<@&?(\d+)>', '', message)

#separates Discord incoming message
def separate_message(message):
    return re.sub(r'[^\w\s]', '', message.strip()).split(' ')

def checking_list_for_empty_str(list: list[str]):
    if not list:
        return

    new_list = []

    for element in list:
        if element != '':
            new_list.append(element)

    return new_list

def checking_for_words(separated_message):
    word_count = int(0)

    for word in separated_message: 
        if en.check(word):
            word_count  = word_count + 1
        elif ru.check(word):
            word_count = word_count + 1

    return word_count

client.run(DISCORD_TOKEN)