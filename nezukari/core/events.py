import logging
import hikari

log = logging.getLogger(__name__)


class EventHandler:
    def __init__(self, bot) -> None:
        self.bot = bot

    async def track_start(self, lavalink, event):
        log.info("Track started on guild: %s", event.guild_id)
        node = await lavalink.get_guild_node(event.guild_id)

        if node:
            data = await node.get_data()
            channel_id = data[event.guild_id]
            channel = self.bot.cache.get_guild_channel(channel_id)

            em = hikari.Embed(
                title="Now Playing",
                description=f"[{node.now_playing.track.info.title}]({node.now_playing.track.info.uri})",
            )

            await channel.send(embed=em)

    async def track_finish(self, lavalink, event):
        log.info("Track finished on guild: %s", event.guild_id)

    async def track_exception(self, lavalink, event):
        log.warning("Track exception event happened on guild: %d", event.guild_id)

        skip = await lavalink.skip(event.guild_id)
        node = await lavalink.get_guild_node(event.guild_id)

        if not skip:
            await event.message.respond("Nothing to skip")
        else:
            if not node.queue and not node.now_playing:
                await lavalink.stop(event.guild_id)
