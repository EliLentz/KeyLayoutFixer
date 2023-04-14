# IMPORT DISCORD.PY. ALLOWS ACCESS TO DISCORD'S API.
import discord
from discord.ext import commands
import re
import enchant
en = enchant.Dict("en_US")
ru = enchant.Dict("ru_RU")

# THE API TOKEN
DISCORD_TOKEN = "MTA5NjQwNzYzNDE2NjQxNTQyMg.Gtux6N.pGrVKWSKHrCpzVY95sc7dtuxEf-xQlyJ5gfHMA"

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

    if client.user in message.mentions:
        separetaed_message = re.sub(r'<@!?(\d+)>|<@&?(\d+)>', '', message.content)
        separetaed_message = re.sub(r'[^\w\s]', '', separetaed_message.strip()).split(' ')
        for word in separetaed_message: 
            if en.check(word):
                await message.channel.send(word + " is an english word")
            elif ru.check(word): await message.channel.send(word + " is a russian word")
            else: await message.channel.send(word + " isn't a russian or english word")

    await client.process_commands(message)

client.run(DISCORD_TOKEN)
