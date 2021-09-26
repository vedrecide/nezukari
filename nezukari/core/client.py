import tanjun
import typing
import hikari

from nezukari.core.bot import Bot


class Client(tanjun.Client):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @classmethod
    def from_gateway_bot(
        cls,
        bot: Bot,
        /,
        *,
        event_managed: bool = True,
        mention_prefix: bool = False,
        set_global_commands: typing.Union[
            hikari.SnowflakeishOr[hikari.PartialGuild]
        ] = 830748949933064202,
    ) -> tanjun.clients.Client:

        client: tanjun.Client = (
            cls(
                rest=bot.rest,
                cache=bot.cache,
                events=bot.event_manager,
                shards=bot,
                event_managed=event_managed,
                mention_prefix=mention_prefix,
                set_global_commands=set_global_commands,
            )
            .set_human_only()
            .set_hikari_trait_injectors(bot)
        )

        return client
