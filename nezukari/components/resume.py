import tanjun

resume_component = tanjun.Component()


@resume_component.with_slash_command
@tanjun.as_slash_command("resume", "Resume the song that is paused")
async def resume(ctx: tanjun.abc.Context) -> None:
    node = await ctx.shards.data.lavalink.get_guild_node(ctx.guild_id)

    if not node or not node.now_playing:
        return await ctx.respond("Nothing is being played at the moment")

    if node.is_paused:
        await ctx.shards.data.lavalink.resume(ctx.guild_id)
        await ctx.respond("Resumed successfully")
    else:
        await ctx.respond("It's already resumed >:(")


@tanjun.as_loader
def load(client: tanjun.Client) -> None:
    client.add_component(resume_component.copy())
