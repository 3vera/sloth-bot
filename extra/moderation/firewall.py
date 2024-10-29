# import.standard
from typing import List

# import.thirdparty
from discord.ext import commands

# import.local
from mysqldb import DatabaseCore

class BypassFirewallTable(commands.Cog):
    """ Category for the BypassFirewall table in the database. """

    def __init__(self, client: commands.Bot) -> None:
        """ Class init method. """

        self.client = client
        self.db = DatabaseCore()

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def create_table_bypass_firewall(self, ctx) -> None:
        """ (ADM) Creates the BypassFirewall table. """

        if await self.check_table_bypass_firewall_exists():
            return await ctx.send("**Table __BypassFirewall__ already exists!**")

        await ctx.message.delete()
        await self.db.execute_query("""
            CREATE TABLE BypassFirewall (
                user_id BIGINT NOT NULL,
                PRIMARY KEY (user_id)
            )""")
        await self.db.execute_query("INSERT INTO Firewall VALUES(0)")

        return await ctx.send("**Table __BypassFirewall__ created!**", delete_after=3)

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def drop_table_bypass_firewall(self, ctx) -> None:
        """ (ADM) Creates the BypassFirewall table """

        if not await self.check_table_bypass_firewall_exists():
            return await ctx.send("**Table __BypassFirewall__ doesn't exist!**")
        await ctx.message.delete()
        await self.db.execute_query("DROP TABLE BypassFirewall")

        return await ctx.send("**Table __BypassFirewall__ dropped!**", delete_after=3)

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def reset_table_bypass_firewall(self, ctx):
        """ (ADM) Resets the BypassFirewall table. """

        if not await self.check_table_bypass_firewall_exists():
            return await ctx.send("**Table __BypassFirewall__ doesn't exist yet**")

        await ctx.message.delete()
        await self.db.execute_query("DELETE FROM BypassFirewall")

        return await ctx.send("**Table __BypassFirewall__ reset!**", delete_after=3)

    # ===== SHOW ===== 
    async def check_table_bypass_firewall_exists(self) -> bool:
        """ Checks if the BypassFirewall table exists """

        return await self.db.table_exists("BypassFirewall")

    # ===== INSERT =====
    async def insert_bypass_firewall_user(self, user_id: int) -> None:
        """ Inserts a user into the BypassFirewall table.
        :param user_id: The ID of the user to insert. """

        await self.db.execute_query("INSERT INTO BypassFirewall (user_id) VALUES (%s)", (user_id,))

    # ===== SELECT =====
    async def get_bypass_firewall_user(self, user_id: int) -> List[int]:
        """ Gets a user from the BypassFirewall table.
        :param user_id: The ID of the user to get. """

        return await self.db.execute_query("SELECT * FROM BypassFirewall WHERE user_id = %s", (user_id,), fetch="one")

    async def get_bypass_firewall_users(self) -> List[List[int]]:
        """ Gets all users from the BypassFirewall table. """

        return await self.db.execute_query("SELECT * FROM BypassFirewall", fetch="all")

    # ===== DELETE =====
    async def delete_bypass_firewall_user(self, user_id: int) -> None:
        """ Deletes a user from the BypassFirewall table.
        :param user_id: The ID of the user to delete. """

        await self.db.execute_query("DELETE FROM BypassFirewall WHERE user_id = %s", (user_id,))


class ModerationFirewallTable(commands.Cog):
    """ Category for the Firewall system and its commands and methods. """

    def __init__(self, client) -> None:
        self.client = client
        self.db = DatabaseCore()

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def create_table_firewall(self, ctx) -> None:
        """ (ADM) Creates the Firewall table. """

        if await self.check_table_firewall_exists():
            return await ctx.send("**Table __Firewall__ already exists!**")

        await ctx.message.delete()
        await self.db.execute_query(
            """CREATE TABLE Firewall (
                state TINYINT(1) NOT NULL DEFAULT 0,
                type VARCHAR(13) DEFAULT 'timeout',
                minimum_account_age INT DEFAULT 43200,
                reason VARCHAR(1300) DEFAULT 'Account is less than 12 hours old.')
            """)
        await self.db.execute_query("INSERT INTO Firewall VALUES(0, 'timeout', 43200, 'Account is less than 12 hours old.')")

        return await ctx.send("**Table __Firewall__ created!**", delete_after=3)

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def drop_table_firewall(self, ctx) -> None:
        """ (ADM) Creates the Firewall table """

        if not await self.check_table_firewall_exists():
            return await ctx.send("**Table __Firewall__ doesn't exist!**")
        await ctx.message.delete()
        await self.db.execute_query("DROP TABLE Firewall")

        return await ctx.send("**Table __Firewall__ dropped!**", delete_after=3)

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def reset_table_firewall(self, ctx):
        """ (ADM) Resets the Firewall table. """

        if not await self.check_table_firewall_exists():
            return await ctx.send("**Table __Firewall__ doesn't exist yet**")

        await ctx.message.delete()
        await self.db.execute_query("DELETE FROM Firewall")
        await self.db.execute_query("INSERT INTO Firewall VALUES(0, 'timeout', 43200, 'Account is less than 12 hours old.')")

        return await ctx.send("**Table __Firewall__ reset!**", delete_after=3)

    async def check_table_firewall_exists(self) -> bool:
        """ Checks if the Firewall table exists """

        return await self.db.table_exists("Firewall")

    async def set_firewall_state(self, state: int) -> None:
        """ Sets the firewall state to either true or false. 
        :param state: The state of the firewall to set. """

        await self.db.execute_query("UPDATE Firewall SET state = %s", (state,))

    async def get_firewall_state(self) -> int:
        """ Gets the firewall's current state. """

        return await self.db.execute_query("SELECT state FROM Firewall", fetch="one")

    async def set_firewall_min_account_age(self, min_age: int) -> int:
        """ Sets the firewall's current minimum account age limit.
        :param min_age: The minimum account age limit to set. """

        await self.db.execute_query("UPDATE Firewall SET minimum_account_age = %s", (min_age,))

    async def get_firewall_min_account_age(self) -> int:
        """ Gets the firewall's current minimum account age limit. """

        return await self.db.execute_query("SELECT minimum_account_age FROM Firewall", fetch="one")

    async def set_firewall_reason(self, reason: str) -> str:
        """ Sets the firewall's current response reason.
        :param reason: The reason to set. """

        await self.db.execute_query("UPDATE Firewall SET reason = %s", (reason,))

    async def get_firewall_reason(self) -> str:
        """ Gets the firewall's current response reason. """

        return await self.db.execute_query("SELECT reason FROM Firewall", fetch="one")

    async def set_firewall_type(self, type: str) -> str:
        """ Sets the firewall's current response type.
        :param type: The type to set. """

        await self.db.execute_query("UPDATE Firewall SET type = %s", (type,))

    async def get_firewall_type(self) -> str:
        """ Gets the firewall's current response type. """

        return await self.db.execute_query("SELECT type FROM Firewall", fetch="one")
