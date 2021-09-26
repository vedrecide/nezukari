import tanjun
import lavasnek_rs

from nezukari.components.join import _join

play_component = tanjun.Component()


@play_component.with_slash_command
@tanjun.with_str_slash_option("song", "Name or URL of the song")
@tanjun.as_slash_command("play", "Play's a song")
async def play(ctx: tanjun.abc.Context, song: str) -> None:
    con = await ctx.shards.data.lavalink.get_guild_gateway_connection_info(ctx.guild_id)

    if not con:
        await _join(ctx)

    query_information = await ctx.shards.data.lavalink.auto_search_tracks(song)

    if not query_information.tracks:
        await ctx.respond("Could not find any video of the search query.")
        return

    try:
        await ctx.shards.data.lavalink.play(
            ctx.guild_id, query_information.tracks[0]
        ).requester(ctx.author.id).queue()
    except lavasnek_rs.NoSessionPresent:
        await ctx.respond("Use `/join` first")
        return

    await ctx.respond(f"Added to queue: {query_information.tracks[0].info.title}")


@tanjun.as_loader
def load(client: tanjun.Client) -> None:
    client.add_component(play_component.copy())
