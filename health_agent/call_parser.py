import json
import os
import openai
import logging
from health_agent.constants import TRANSCRIPT_CONTENT

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class CallParser:
    def __init__(self, call_transcript):
        self.transcript = call_transcript
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def parse_transcript(self, patient_data_structure: dict):
        output_json_string = json.dumps(patient_data_structure)
        chatcompletion_config = {
            "model": "gpt-4",
            "temperature": 0,
            "messages": [
                {
                    "role": "system",
                    "content": TRANSCRIPT_CONTENT + output_json_string,
                },
                {
                    "role": "user",
                    "content": self.transcript,
                },
            ],
        }
        try:
            logger.debug("PARSING TRANSCRIPT")
            chat_completion_result = openai.ChatCompletion.create(
                **chatcompletion_config
            )
        except Exception as e:
            logger.error(
                f"Error while parsing transcript, openAIclient.chat.completions.create error: {e}"
            )
            return

        chat_completion_result_content = ""
        if not chat_completion_result.choices[0]:
            logger.error(f"Reply from openAIclient.chat.completions assistant is empty")
        else:
            chat_completion_result_content = chat_completion_result.choices[
                0
            ].message.content

        return json.loads(chat_completion_result_content)
