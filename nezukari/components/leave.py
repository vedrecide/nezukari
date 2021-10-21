import tanjun
import hikari

from typing import Union

leave_component = tanjun.Component()


@leave_component.with_slash_command
@tanjun.as_slash_command("leave", "Leave's a voice channel", default_to_ephemeral=True)
async def leave(ctx: tanjun.abc.Context) -> Union[hikari.Message, None]:
    node = await ctx.shards.data.lavalink.get_guild_node(ctx.guild_id)

    await ctx.shards.data.lavalink.destroy(ctx.guild_id)
    await ctx.shards.data.lavalink.leave(ctx.guild_id)
    await ctx.shards.data.lavalink.remove_guild_node(ctx.guild_id)
    await ctx.shards.data.lavalink.remove_guild_from_loops(ctx.guild_id)

    await ctx.respond("Left the Voice channel")


@tanjun.as_loader
def load(client: tanjun.Client) -> None:
    client.add_component(leave_component.copy())
