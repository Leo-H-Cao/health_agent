import typing
from vocode.streaming.utils import events_manager
from vocode.streaming.models.events import Event, EventType
from vocode.streaming.models.transcript import TranscriptCompleteEvent
from health_agent.constants import CALLER_WITH_APPOINTMENT
from health_agent.call_parser import CallParser
from health_agent.outbound_email import OutboundEmail
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class CustomEventsManager(events_manager.EventsManager):
    def __init__(self):
        super().__init__(subscriptions=[EventType.TRANSCRIPT_COMPLETE])

    def handle_event(self, event: Event):
        if event.type == EventType.TRANSCRIPT_COMPLETE:
            logger.debug("Handling Transcription Complete Event")
            transcript_complete_event = typing.cast(TranscriptCompleteEvent, event)
            self.process_transcript(transcript_complete_event)

    def process_transcript(self, transcript_complete_event: TranscriptCompleteEvent):
        call_transcript = transcript_complete_event.transcript.to_string(
            include_timestamps=False
        )
        transcript_parser = CallParser(call_transcript)
        patient_json = transcript_parser.parse_transcript(CALLER_WITH_APPOINTMENT)

        if not patient_json:
            logger.error("Error: could not parse transcript to patient data JSON")
            return
        logger.info(patient_json)

        first_name = patient_json.get("first_name")
        email = patient_json.get("contact").get("email")
        appointment_info = patient_json.get("appointment_info")

        email_sender = OutboundEmail()
        logger.debug("Parsed Patient email: " + email)
        email_sender.send_appointment_email(email, first_name, appointment_info)
