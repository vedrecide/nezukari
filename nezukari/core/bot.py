import hikari
import lavasnek_rs

from nezukari.core.config import Config
from nezukari.core.events import EventHandler


class Data:
    def __init__(self) -> None:
        self.lavalink: lavasnek_rs.Lavalink = None


class Bot(hikari.GatewayBot):
    def __init__(self) -> None:
        super().__init__(token=Config.token)
        self.event_manager.subscribe(hikari.ShardReadyEvent, self.on_started)
        self.data = Data()

    async def on_started(self, _: hikari.ShardReadyEvent) -> None:
        builder = (
            lavasnek_rs.LavalinkBuilder(_.my_user.id, Config.token)
            .set_host(Config.host).set_password(Config.password)
        )
        lava_client = await builder.build(EventHandler())
        self.data.lavalink = lava_client

    def run(self) -> None:
        super().run()
