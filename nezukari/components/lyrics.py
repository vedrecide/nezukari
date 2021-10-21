import tanjun
import hikari
import aiohttp
import yuyo

from typing import Optional, Union

from yuyo import components


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

        pages = (
            (
                hikari.UNDEFINED,
                hikari.Embed(
                    title=f'Search result for "{song}"', description=page
                ).set_footer(text=f"Page {index + 1}"),
            )
            for page, index in yuyo.sync_paginate_string(
                iter(lyrics.splitlines()), line_limit=15
            )
        )

        res = yuyo.ComponentPaginator(pages, authors=[ctx.author.id])

        if not (first_response := await res.get_next_entry()):
            pass

        content, embed = first_response
        message = await ctx.respond(
            content=content, embed=embed, component=res, ensure_result=True
        )
        ctx.shards.component_client.add_executor(message, res)
    else:
        if not node or not node.now_playing:
            return await ctx.respond("No song is being played not right now")

        lyrics = await get_lyrics(node.now_playing.track.info.title)
        if lyrics == "Couldn't find the lyrics":
            return await ctx.respond("Couldn't find the lyrics, sorry :c")

        pages = (
            (
                hikari.UNDEFINED,
                hikari.Embed(description=page)
                .set_author(
                    name=f"{node.now_playing.track.info.title}",
                    url=f"{node.now_playing.track.info.uri}",
                )
                .set_footer(text=f"Page {index + 1}"),
            )
            for page, index in yuyo.sync_paginate_string(
                iter(lyrics.splitlines()), line_limit=15
            )
        )

        res = yuyo.ComponentPaginator(
            pages,
            authors=[ctx.author.id],
            triggers=(
                yuyo.pagination.LEFT_DOUBLE_TRIANGLE,
                yuyo.pagination.LEFT_TRIANGLE,
                yuyo.pagination.STOP_SQUARE,
                yuyo.pagination.RIGHT_TRIANGLE,
                yuyo.pagination.RIGHT_DOUBLE_TRIANGLE,
            ),
        )

        if not (first_response := await res.get_next_entry()):
            pass

        content, embed = first_response
        message = await ctx.respond(
            content=content, embed=embed, component=res, ensure_result=True
        )
        ctx.shards.component_client.add_executor(message, res)


@tanjun.as_loader
def load(client: tanjun.Client) -> None:
    client.add_component(lyric_component.copy())
