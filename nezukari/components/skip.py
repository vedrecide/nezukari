import tanjun
import hikari

from typing import Union

skip_component = tanjun.Component()

@skip_component.with_slash_command
@tanjun.as_slash_command("skip", "Skip's the current song")
async def skip(ctx: tanjun.abc.Context) -> Union[hikari.Message, None]:

    skip = await ctx.shards.data.lavalink.skip(ctx.guild_id)
    node = await ctx.shards.data.lavalink.get_guild_node(ctx.guild_id)

    if not skip:
        return await ctx.respond("Nothing to skip")

    if not node.queue and not node.now_playing:
        await ctx.shards.data.lavalink.stop(ctx.guild_id)

    em = hikari.Embed(
        title="Skipped",
        description=f"[{skip.track.info.title}]({skip.track.info.uri})"
    )

    await ctx.respond(embed=em)

@tanjun.as_loader
def load(client: tanjun.Client) -> None:
    client.add_component(skip_component.copy())
