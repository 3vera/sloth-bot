import discord
from discord.ext import commands

from extra import utils
from random import randint
import os

bots_and_commands_channel_id: int = int(os.getenv('BOTS_AND_COMMANDS_CHANNEL_ID', 123))
server_id: int = int(os.getenv('SERVER_ID', 123))

async def quest_one_callback(client: commands.Bot, user_id: int) -> None:
    """ Callback for the quest one.
    :param client: The bot client.
    :param user_id: The user ID. """

    pass

async def quest_two_callback(client: commands.Bot, user_id: int) -> None:
    """ Callback for the quest two.
    :param client: The bot client.
    :param user_id: The user ID. """

    pass

async def quest_three_callback(client: commands.Bot, user_id: int) -> None:
    """ Callback for the quest_three.
    :param client: The bot client.
    :param user_id: The user ID. """

    pass

async def quest_four_callback(client: commands.Bot, user_id: int) -> None:
    """ Callback for the quest four.
    :param client: The bot client.
    :param user_id: The user ID. """

    pass

async def quest_five_callback(client: commands.Bot, user_id: int) -> None:
    """ Callback for the quest five.
    :param client: The bot client.
    :param user_id: The user ID. """

    pass

async def quest_six_callback(client: commands.Bot, user_id: int) -> None:
    """ Callback for the quest six.
    :param client: The bot client.
    :param user_id: The user ID. """

    # Gets general info
    current_time = await utils.get_time_now()
    money = 100
    guild = client.get_guild(server_id)
    member = guild.get_member(user_id)
    cog = client.get_cog('SlothClass')

    # Gets user profile
    sloth_profile = await cog.get_sloth_profile(member.id)
    if not sloth_profile:
        return

    # Gets user tribe
    tribe = await cog.get_tribe_info_by_name(sloth_profile[3])
    if not tribe:
        return
    
    tribe_members = await cog.get_tribe_members(tribe_name=tribe['name'])
    all_users = list(map(lambda mid: (money, mid[0]), tribe_members))

    await client.get_cog('SlothCurrency').update_user_many_money(all_users)
    bots_and_commands_channel = guild.get_channel(bots_and_commands_channel_id)

    # Makes embed
    embed = discord.Embed(
        title="__Quest Six Complete__",
        description=f"{member.mention} and all members of his tribe named `{tribe['name']}` got `{money}`łł" \
            f" for completing the `Quest six`! 🍃🍃",
        color=discord.Color.green(),
        timestamp=current_time
    )
    embed.set_author(name=f"Tribe: {tribe['name']}", url=tribe["link"])
    if tribe_tn := tribe.get('thumbnail'):
        embed.set_thumbnail(url=tribe_tn)
    embed.set_footer(text=f"Completed by: {member}", icon_url=member.display_avatar)

    await bots_and_commands_channel.send(embed=embed)