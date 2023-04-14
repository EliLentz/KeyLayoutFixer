# IMPORT DISCORD.PY. ALLOWS ACCESS TO DISCORD'S API.
import discord
from discord.ext import commands

# GRAB THE API TOKEN FROM THE .ENV FILE.
DISCORD_TOKEN = "MTA5NjQwNzYzNDE2NjQxNTQyMg.GK8q_8.Hz_mmuLd-Q_jhE4r0RZGguf6JlVktErUPYCvVc"

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.reactions = True
client = commands.Bot(command_prefix='!', intents=intents)

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

    print("SampleDiscordBot is in " + str(guild_count) + " guilds.")


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

    await client.process_commands(message)

client.run(DISCORD_TOKEN)
