#anemometer python code
import subprocess
import asyncio
import logging
import paho.mqtt.client as mqtt
import datetime

from modules.data_models.mqtt_packets import MQTTPositionPkt, MQTTSpeedPkt, SenderTypes,MQTTwindPkt
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
#dt = datetime.datetime.utcnow()
#parsed_msg: NMEAMessage = None
# _, parsed_msg = self.nmea_stream.read()

def retry_policy(info: RetryInfo) -> RetryPolicyStrategy:
    return False, (info.fails - 1) % 3 * 0.1

@retry(retry_policy)
async def calypso_subscribe_demo():
    def process_reading(reading:CalypsoReading):
       
        reading.dump()
        dt = datetime.datetime.utcnow()
        wind_Pkt= MQTTwindPkt(
                timestamp =int(dt.timestamp()), #int
                sender_type = SenderTypes.wind, #str
                #name = "calypso_anemo",       #st
                wind_spd= reading.wind_speed,  #float
                wind_dir= reading.wind_direction #int
                      
            )
        client.publish(MqttTopics.WIND,str(wind_Pkt))

    
    async with CalypsoDeviceApi(settings=Settings(ble_discovery_timeout=5, ble_connect_timeout=20)) as calypso:
        client = MqttPubModule([MqttTopics.WIND])
        
        await calypso.subscribe_reading(process_reading)
        await wait_forever()
        #await calypso.discover()
        #await calypso.connect()

        await calypso.about()



if __name__ == "__main__":  # pragma: nocover
    asyncio.run(calypso_subscribe_demo())