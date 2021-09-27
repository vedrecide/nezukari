import tanjun
import hikari

from typing import Union

nowplaying_component = tanjun.Component()


@nowplaying_component.with_slash_command
@tanjun.as_slash_command("nowplaying", "Show's the song that is being played right now")
async def nowplaying(ctx: tanjun.abc.Context) -> Union[hikari.Message, None]:
    node = await ctx.shards.data.lavalink.get_guild_node(ctx.guild_id)

    if not node or not node.now_playing:
        return await ctx.respond("Nothing is being played at the moment")

    em = hikari.Embed(
        title="Now playing",
        description=f"[{node.now_playing.track.info.title}]({node.now_playing.track.info.uri})",
    )

    await ctx.respond(embed=em)


@tanjun.as_loader
def load(client: tanjun.Client) -> None:
    client.add_component(nowplaying_component.copy())
