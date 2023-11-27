import discord
from discord.ext import commands
from dotenv import load_dotenv
import enchant
import json
import re
import os

eng_dictionary = enchant.Dict("en_US")
rus_dictionary = enchant.Dict("ru_RU")


def load_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


eng_keys = load_json_file('./Languages/english.json')
rus_keys = load_json_file('./Languages/russian.json')

# LOADS THE .ENV FILE THAT RESIDES ON THE SAME LEVEL AS THE SCRIPT.
load_dotenv()

# THE API TOKEN
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.reactions = True
client = commands.Bot(command_prefix='/', intents=intents)

emoji = '\N{THUMBS UP SIGN}'


def switch_keyboard_layout(text, layout_mapping_from: dict[str, str], layout_mapping_to: dict[str, str]):
    layout_keys = list(layout_mapping_from.values())
    layout_values = list(layout_mapping_to.values())

    layout_mapping: dict[str, str] = {}
    for key in layout_keys:
        for value in layout_values:
            layout_mapping[key] = value
            layout_values.remove(value)
            break

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
async def languages(ctx):
    await ctx.send(enchant.list_languages())


@client.command()
async def convert(ctx):
    if ctx.message.reference is not None:
        # Get the replied message
        replied_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)

        await ctx.message.add_reaction(emoji)

        # Try converting with both layouts and pick the one with more English characters
        eng_converted = switch_keyboard_layout(
            replied_message.content, rus_keys, eng_keys)
        rus_converted = switch_keyboard_layout(
            replied_message.content, eng_keys, rus_keys)

        eng_converted_inequality = checking_for_equal_chars(
            replied_message.content, eng_converted)
        rus_converted_inequality = checking_for_equal_chars(
            replied_message.content, rus_converted)

        if eng_converted_inequality > rus_converted_inequality:
            await ctx.send(eng_converted)
        else:
            await ctx.send(rus_converted)

    else:
        await ctx.send("Please reply to a message with the !convert command to convert the text.")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    message_without_mention = delete_mention(message.content)

    separated_message_without_mention = separate_message(
        message_without_mention)

    message_words_checked = checking_for_words(
        separated_message_without_mention)

    eng_converted = switch_keyboard_layout(
        message_without_mention, rus_keys, eng_keys)
    rus_converted = switch_keyboard_layout(
        message_without_mention, eng_keys, rus_keys)

    separated_eng_message = checking_list_for_empty_str(
        separate_message(eng_converted))
    separated_rus_message = checking_list_for_empty_str(
        separate_message(rus_converted))

    if separated_eng_message and separated_rus_message:
        rus_words_checked = checking_for_words(separated_rus_message)
        eng_words_checked = checking_for_words(separated_eng_message)

        if eng_words_checked > rus_words_checked:
            if message_words_checked != eng_words_checked:
                await message.channel.send(eng_converted)
        elif rus_words_checked > eng_words_checked:
            if message_words_checked != rus_words_checked:
                await message.channel.send(rus_converted)

    await client.process_commands(message)


def delete_mention(message):
    return re.sub(r'<@!?(\d+)>|<@&?(\d+)>', '', message)

# separates Discord incoming message


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


def checking_for_words(separated_message: list):
    word_count = int(0)

    for word in separated_message:
        if eng_dictionary.check(word):
            word_count = word_count + 1
        elif rus_dictionary.check(word):
            word_count = word_count + 1

    return word_count


def checking_for_equal_chars(message: str, converted_message: str):
    count_of_inequality = 0

    for i in range(len(message)):
        if message[i] != converted_message[i]:
            count_of_inequality += 1
    return count_of_inequality


client.run(DISCORD_TOKEN)
