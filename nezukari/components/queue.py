import tanjun
import hikari

from typing import Union

queue_component = tanjun.Component()


@queue_component.with_slash_command
@tanjun.as_slash_command("queue", "Show's the music queue")
async def queue(ctx: tanjun.abc.Context) -> Union[hikari.Message, None]:

    node = await ctx.shards.data.lavalink.get_guild_node(ctx.guild_id)

    if not node:
        return await ctx.respond("Nothing in the Queue")
    else:
        code_blocks = None
        for songs in node.queue:
            queued_songs = "".join(a.track.info.title + "\n" for a in node.queue)
            code_blocks = queued_songs

        await ctx.respond(f"```{code_blocks}```")


@tanjun.as_loader
def load(client: tanjun.Client) -> None:
    client.add_component(queue_component.copy())
