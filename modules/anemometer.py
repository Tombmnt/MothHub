#anemometer python code
import subprocess
import asyncio
import logging

from modules.data_models.mqtt_packets import MQTTPositionPkt, MQTTSpeedPkt, SenderTypes
from .mqtt_utils import MqttTopics
from .mqtt_modules import MqttPubModule
from calypso_anemometer.core import CalypsoDeviceApi, Settings
from calypso_anemometer.model import CalypsoReading
from calypso_anemometer.util import wait_forever
from  calypso_anemometer.exception import*
from calypso_anemometer.util import setup_logging


from aioretry import  retry,RetryPolicyStrategy,RetryInfo

   


logger = logging.getLogger(__name__)
#setup_logging(level=logging.DEBUG)
def retry_policy(info: RetryInfo) -> RetryPolicyStrategy:
    return False, (info.fails - 1) % 3 * 0.1

@retry(retry_policy)
async def calypso_subscribe_demo():
    def process_reading(reading: CalypsoReading):
        reading.dump()

   
    async with CalypsoDeviceApi(settings=Settings(ble_discovery_timeout=5, ble_connect_timeout=20)) as calypso:

        await calypso.subscribe_reading(process_reading)
        await wait_forever()
        #await calypso.discover()
        #await calypso.connect()

        await calypso.about()


if __name__ == "__main__":  # pragma: nocover
    asyncio.run(calypso_subscribe_demo())