import logging
import os
import sys

from fastapi import FastAPI
from vocode.streaming.models.telephony import TwilioConfig
from pyngrok import ngrok
from vocode.streaming.telephony.config_manager.redis_config_manager import (
    RedisConfigManager,
)
from vocode.streaming.models.agent import ChatGPTAgentConfig
from vocode.streaming.models.message import BaseMessage
from vocode.streaming.telephony.server.base import (
    TwilioInboundCallConfig,
    TelephonyServer,
)
from dotenv import load_dotenv
from vocode.streaming.models.transcriber import (
    DEFAULT_SAMPLING_RATE,
    DEFAULT_AUDIO_ENCODING,
    DEFAULT_CHUNK_SIZE,
)

from vocode.streaming.telephony.config_manager.in_memory_config_manager import (
    InMemoryConfigManager,
)
from health_agent.constants import INITIAL_MESSAGE, PROMPT_PREAMBLE
from vocode.streaming.models.transcriber import (
    DeepgramTranscriberConfig,
    PunctuationEndpointingConfig,
)
from vocode.streaming.models.synthesizer import AzureSynthesizerConfig
from vocode.streaming.models.synthesizer import (
    DEFAULT_SAMPLING_RATE,
    DEFAULT_AUDIO_ENCODING,
)
from health_agent.custom_events_manager import CustomEventsManager


load_dotenv()

app = FastAPI(docs_url=None)

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

config_manager = InMemoryConfigManager()

BASE_URL = os.getenv("BASE_URL")

if not BASE_URL:
    ngrok_auth = os.environ.get("NGROK_AUTH_TOKEN")
    if ngrok_auth is not None:
        ngrok.set_auth_token(ngrok_auth)
    port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else 3000

    # Open a ngrok tunnel to the dev server
    BASE_URL = ngrok.connect(port).public_url.replace("https://", "")
    logger.info('ngrok tunnel "{}" -> "http://127.0.0.1:{}"'.format(BASE_URL, port))

if not BASE_URL:
    raise ValueError("BASE_URL must be set in environment if not using pyngrok")

deepgram_config = DeepgramTranscriberConfig(
    endpointing_config=PunctuationEndpointingConfig(),
    sampling_rate=DEFAULT_SAMPLING_RATE,
    audio_encoding=DEFAULT_AUDIO_ENCODING,
    chunk_size=DEFAULT_CHUNK_SIZE,
)

gpt_agent_config = ChatGPTAgentConfig(
    prompt_preamble=PROMPT_PREAMBLE,
    initial_message=BaseMessage(text=INITIAL_MESSAGE),
    generate_responses=True,
    allow_agent_to_be_cut_off=False,
)

azure_synthesizer_config = AzureSynthesizerConfig(
    sampling_rate=DEFAULT_SAMPLING_RATE,
    audio_encoding=DEFAULT_AUDIO_ENCODING,
    azure_speech_key=os.environ["AZURE_SPEECH_KEY"],
    azure_speech_region=os.environ["AZURE_SPEECH_REGION"],
    voice_name="en-US-ChristopherNeural",
)

twilio_inbound_call_config = TwilioInboundCallConfig(
    url="/inbound_call",
    agent_config=gpt_agent_config,
    transcriber_config=deepgram_config,
    twilio_config=TwilioConfig(
        account_sid=os.environ["TWILIO_ACCOUNT_SID"],
        auth_token=os.environ["TWILIO_AUTH_TOKEN"],
    ),
    logger=logger,
    synthesizer_config=azure_synthesizer_config,
)

custom_events_manager = CustomEventsManager()

telephony_server = TelephonyServer(
    base_url=BASE_URL,
    config_manager=config_manager,
    inbound_call_configs=[twilio_inbound_call_config],
    logger=logger,
    events_manager=custom_events_manager,
)

app.include_router(telephony_server.get_router())
