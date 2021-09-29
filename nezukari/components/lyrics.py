import tanjun
import hikari
import aiohttp

from typing import Optional, Union


async def get_lyrics(name: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://some-random-api.ml/lyrics?title={name}") as r:
            res = await r.json()
            try:
                return res["lyrics"]
            except KeyError:
                return "Couldn't find the lyrics"


lyric_component = tanjun.Component()


@lyric_component.with_slash_command
@tanjun.with_str_slash_option("song", "Name of the song", default=None)
@tanjun.as_slash_command(
    "lyrics",
    "Show's the lyrics of the song playing right now or the one mentioned in the arguments",
)
async def lyrics_command(
    ctx: tanjun.abc.Context, song: Optional[str]
) -> Union[hikari.Message, None]:
    node = await ctx.shards.data.lavalink.get_guild_node(ctx.guild_id)

    if song:
        lyrics = await get_lyrics(name=song)
        if lyrics == "Couldn't find the lyrics":
            return await ctx.respond("Couldn't find the lyrics, sorry :c")

        em = hikari.Embed(description=lyrics).set_author(name=f'Lyrics of "{song}"')
        await ctx.respond(embed=em)
    else:
        if not node or not node.now_playing:
            return await ctx.respond("No song is being played not right now")

        lyrics = await get_lyrics(node.now_playing.track.info.title)
        if lyrics == "Couldn't find the lyrics":
            return await ctx.respond("Couldn't find the lyrics, sorry :c")

        em = hikari.Embed(description=lyrics).set_author(
            name=f"{node.now_playing.track.info.title}",
            url=f"{node.now_playing.track.info.uri}",
        )
        await ctx.respond(embed=em)


@tanjun.as_loader
def load(client: tanjun.Client) -> None:
    client.add_component(lyric_component.copy())
