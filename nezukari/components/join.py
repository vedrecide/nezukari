import tanjun

join_component = tanjun.Component()

async def _join(ctx: tanjun.abc.Context) -> int:
    states = ctx.shards.cache.get_voice_states_view_for_guild(ctx.get_guild())
    voice_state = list(filter(lambda i: i.user_id == ctx.author.id, states.iterator()))

    if not voice_state:
        await ctx.respond("Connect to a voice channel first")
        return 0

    channel_id = voice_state[0].channel_id

    try:
        connection_info = await ctx.shards.data.lavalink.join(ctx.guild_id, channel_id)
    except TimeoutError:
        await ctx.respond(
            "I was unable to connect to the voice channel, maybe missing permissions? or some internal issue."
        )
        return 0

    await ctx.shards.data.lavalink.create_session(connection_info)
    return channel_id

@join_component.with_slash_command
@tanjun.as_slash_command("join", "Join's a voice channel")
async def join(ctx: tanjun.abc.Context) -> None:
    channel_id = await _join(ctx)

    if channel_id:
        await ctx.respond(f"Joined <#{channel_id}>")

@tanjun.as_loader
def load(client: tanjun.Client) -> None:
    client.add_component(join_component.copy())
