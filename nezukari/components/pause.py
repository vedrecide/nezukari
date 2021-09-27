import tanjun

pause_component = tanjun.Component()


@pause_component.with_slash_command
@tanjun.as_slash_command("pause", "Pause the current song being played")
async def pause(ctx: tanjun.abc.Context) -> None:
    node = await ctx.shards.data.lavalink.get_guild_node(ctx.guild_id)

    if not node or not node.now_playing:
        return await ctx.respond("Nothing is being played at the moment")

    await ctx.shards.data.lavalink.pause(ctx.guild_id)
    await ctx.respond("Paused successfully")


@tanjun.as_loader
def load(client: tanjun.Client) -> None:
    client.add_component(pause_component.copy())
