import discord
import aiohttp
from os import getenv
from discord import app_commands
from discord.ext import commands, tasks
from typing import Literal

from utilities.embedhandler import EmbedHandler

GUILD_ID = getenv("DEV_SERVER_ID")

class PriceAlert(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.hypixel_api_key = getenv("HYPIXEL_API_KEY")
        
        
        self.http_session = None
        self.bazaar_cache = {}

        if not self.hypixel_api_key:
            print("HYPIXEL_API_KEY not found, PriceAlert cog will not work")
            return 

        self.http_session = aiohttp.ClientSession()
        self.update_bazaar_cache.start()
        self.check_prices.start()

    def cog_unload(self):
        
        if self.update_bazaar_cache.is_running():
            self.update_bazaar_cache.cancel()
        if self.check_prices.is_running():
            self.check_prices.cancel()
        
        
        if self.http_session:
            self.bot.loop.create_task(self.http_session.close())


    @commands.Cog.listener()
    async def on_ready(self):
        print("PriceAlert cog loaded and ready.")

    @tasks.loop(minutes=1)
    async def update_bazaar_cache(self):
        url = f"https://api.hypixel.net/v2/skyblock/bazaar?key={self.hypixel_api_key}"
        try:
            async with self.http_session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("success"):
                        self.bazaar_cache = data.get("products", {})
                        print("Bazaar data updated successfully")
                    else:
                        print(f"Hypixel API Error: {data.get('cause')}")
                else:
                    print(f"Failed to update Bazaar cache. Status: {response.status}")
        except Exception as e:
            print(f"An error occurred during Bazaar cache update: {e}")

    @tasks.loop(minutes=1, seconds=5) 
    async def check_prices(self):
        if not self.bazaar_cache:
            return 

        alerts_to_remove = []
        
        async with self.bot.database.cursor() as cursor:
            await cursor.execute("SELECT list_id, user_id, item_name, condition, threshold, track_type FROM prices")
            all_alerts = await cursor.fetchall()

            for alert in all_alerts:
                list_id, user_id, item_name, condition, threshold, track_type = alert
                
                item_id = item_name.upper().replace(" ", "_")
                
                product = self.bazaar_cache.get(item_id)
                if not product:
                    continue # did not find item

                # fetching useful data for msgs

                instant_sell_price = product.get("buy_summary", [{}])[0].get("pricePerUnit")
                instant_buy_price = product.get("sell_summary", [{}])[0].get("pricePerUnit")

                

                if track_type == "Sell Order":
                    tracked_price = instant_buy_price
                else:
                    tracked_price = instant_sell_price

                if tracked_price is None:
                    continue

                triggered = False
                if condition == "below" and tracked_price <= threshold:
                    triggered = True
                elif condition == "above" and tracked_price >= threshold:
                    triggered = True

                if triggered:
                    try:
                        user = await self.bot.fetch_user(user_id)
                        embed = EmbedHandler.new(
                            title="Bazaar Price Alert",
                            description=f"Price Data for your tracked item {item_name} \nInstant Sell Price: **{instant_sell_price:,.1f}** coins\nInstant Buy Price: **{instant_buy_price:,.1f}** coins\n Set threshold: {threshold:,.1f} coins",
                            embed_type="system"
                        )
                        await user.send(embed=embed)
                        alerts_to_remove.append(list_id)
                    except discord.Forbidden:
                        print(f"DM to user {user_id} failed. Alert removed")
                        alerts_to_remove.append(list_id)
                    except Exception as e:
                        print(f"An error occurred sending DM to {user_id}: {e}")

            if alerts_to_remove:
                placeholders = ', '.join('?' for _ in alerts_to_remove)
                await cursor.execute(f"DELETE FROM prices WHERE list_id IN ({placeholders})", alerts_to_remove)
                await self.bot.database.commit()

    @check_prices.before_loop
    @update_bazaar_cache.before_loop
    async def before_loops(self):
        await self.bot.wait_until_ready()

    @app_commands.command(name="bzalert", description="Set a price alert for a Bazaar item.")
    @app_commands.describe(
        item_name="The name of the Bazaar item to track.",
        condition="Alert when the price is above or below your target.",
        price="Your target price.",
        track_type="Track sell price or buy price"
    )
    @app_commands.rename(item_name="item")
    async def set_bz_alert(self, interaction: discord.Interaction, item_name: str, condition: Literal["above", "below"], price: float, track_type: Literal["Buy Order", "Sell Order"]):
        user_id = interaction.user.id
        
        async with self.bot.database.cursor() as cursor:
            await cursor.execute(
                "INSERT INTO prices (user_id, item_name, condition, threshold, track_type) VALUES (?, ?, ?, ?, ?)",
                (user_id, item_name.lower(), condition, price, track_type)
            )
        await self.bot.database.commit()
        embed = EmbedHandler.new(
            title=f"You are now tracking item {item_name}.",
            description=f"You will be notified when the item price goes **{condition}** **{price:,.1f}** coins.",
            embed_type="system",
            footer="work in progress"
        )
        product_data = self.bazaar_cache.get(item_name.upper().replace(' ', '_'), {})
        current_sell_price = product_data.get('buy_summary', [{}])[0].get('pricePerUnit', 0)
        current_buy_price = product_data.get('sell_summary', [{}])[0].get('pricePerUnit', 0)

        embed.add_field(name="Current Prices:", value=f"Sell Order: **{current_buy_price:,.1f}** coins\nBuy Order: **{current_sell_price:,.1f}** coins", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    cog = PriceAlert(bot)
    await bot.add_cog(cog)

    guild_obj = discord.Object(id=GUILD_ID)
    bot.tree.add_command(cog.set_bz_alert, guild=guild_obj)