import tanjun
import hikari
import lavasnek_rs

from nezukari.utils.equalizers import Equalizers
from typing import Union

filter_component = tanjun.Component()


@filter_component.with_slash_command
@tanjun.with_str_slash_option(
    "filter_name", "Name of the filter", choices=("flat", "boost", "metal", "piano")
)
@tanjun.as_slash_command("filter", "Add a filter to the current song")
async def filter(
    ctx: tanjun.abc.Context, filter_name: str
) -> Union[hikari.Message, None]:
    node = await ctx.shards.data.lavalink.get_guild_node(ctx.guild_id)

    if not node or not node.now_playing:
        return await ctx.respond("No song playing right now")

    if filter_name == "flat":
        await ctx.shards.data.lavalink.equalize_all(ctx.guild_id, Equalizers().flat())
        await ctx.respond(f"Applied the filter `{filter_name}` successfully")
    elif filter_name == "boost":
        await ctx.shards.data.lavalink.equalize_all(ctx.guild_id, Equalizers().boost())
        await ctx.respond(f"Applied the filter `{filter_name}` successfully")
    elif filter_name == "metal":
        await ctx.shards.data.lavalink.equalize_all(ctx.guild_id, Equalizers().metal())
        await ctx.respond(f"Applied the filter `{filter_name}` successfully")
    elif filter_name == "piano":
        await ctx.shards.data.lavalink.equalize_all(ctx.guild_id, Equalizers().piano())
        await ctx.respond(f"Applied the filter `{filter_name}` successfully")
    else:
        pass


@tanjun.as_loader
def load(client: tanjun.Client) -> None:
    client.add_component(filter_component.copy())
