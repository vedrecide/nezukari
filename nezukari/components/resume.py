import tanjun

resume_component = tanjun.Component()

@resume_component.with_slash_command
@tanjun.as_slash_command("resume", "Resume the song that is paused")
async def resume(ctx: tanjun.abc.Contex) -> None:
    node = await ctx.shards.data.lavalink.get_guild_node(ctx.guild_id)
    
    if not node or not node.now_playing:
        return await ctx.respond("Nothing is being played at the moment")

    await ctx.shards.data.lavalink.resume(ctx.guild_id)
    await ctx.respond(f"Resumed successfully")

@tanjun.as_loader
def load(client: tanjun.Client) -> None:
    client.add_component(resume_component.copy())
