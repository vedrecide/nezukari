import tanjun
import hikari

from typing import Union

volume_component = tanjun.Component()


@volume_component.with_slash_command
@tanjun.with_int_slash_option("volume", "Volume to be set (Between 0 and 100)")
@tanjun.as_slash_command("volume", "Increase/Decrease the volume")
async def volume(ctx: tanjun.abc.Context, volume: int) -> Union[hikari.Message, None]:
    node = await ctx.shards.data.lavalink.get_guild_node(ctx.guild_id)

    if not node or not node.now_playing:
        return await ctx.respond("Nothing is being played at the moment")

    if 0 < volume < 100:
        return await ctx.respond("Volume should be between 0 and 100")

    await ctx.shards.data.lavalink.volume(ctx.guild_id, volume)
    await ctx.respond(f"Set the volume to {volume}")


@tanjun.as_loader
def load(client: tanjun.Client) -> None:
    client.add_component(client.copy())
