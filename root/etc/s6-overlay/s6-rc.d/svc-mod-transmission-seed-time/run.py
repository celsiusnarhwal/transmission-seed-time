#!/usr/bin/with-contenv python

import time
from datetime import datetime

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from transmission_rpc import Client, IdleMode


class ModSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="TR_")

    minimum_seeding_time: int = Field(0, ge=0)
    idle_seeding_limit: int = Field(0, ge=0)


settings = ModSettings()
tc = Client()

while True:
    print("test")
    for torrent in tc.get_torrents():
        minutes_since_done = (
            datetime.now().astimezone() - torrent.done_date
        ).total_seconds() / 60

        if minutes_since_done >= settings.minimum_seeding_time:
            tc.change_torrent(
                torrent.info_hash,
                seed_idle_limit=settings.idle_seeding_limit,
                seed_idle_mode=IdleMode.Single,
            )

    time.sleep(5)
