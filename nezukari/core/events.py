import logging

log = logging.getLogger(__name__)


class EventHandler:

    async def track_start(self, _lava_client, event):
        log.info("Track started on guild: %s", event.guild_id)

    async def track_finish(self, _lava_client, event):
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
