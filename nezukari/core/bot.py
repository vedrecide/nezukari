import hikari
import lavasnek_rs
import yuyo

from nezukari.core.config import Config
from nezukari.core.events import EventHandler


class Data:
    def __init__(self) -> None:
        self.lavalink: lavasnek_rs.Lavalink = None


class Bot(hikari.GatewayBot):
    def __init__(self) -> None:
        super().__init__(token=Config.token)
        self.component_client = yuyo.ComponentClient(event_manager=self.event_manager)
        self.event_manager.subscribe(hikari.ShardReadyEvent, self.on_started)
        self.event_manager.subscribe(hikari.StartedEvent, self.on_starting)
        self.event_manager.subscribe(hikari.StoppingEvent, self.on_stopping)
        self.data = Data()

    async def on_starting(self, _: hikari.StartedEvent) -> None:
        self.component_client.open()

    async def on_stopping(self, _: hikari.StoppingEvent) -> None:
        self.component_client.close()

    async def on_started(self, _: hikari.ShardReadyEvent) -> None:
        builder = (
            lavasnek_rs.LavalinkBuilder(_.my_user.id, Config.token)
            .set_host(Config.host)
            .set_password(Config.password)
        )
        event_handler = EventHandler(self)
        lava_client = await builder.build(event_handler)
        self.data.lavalink = lava_client

    def run(self) -> None:
        super().run()
