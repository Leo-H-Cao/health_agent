CALLER_INFO_NEEDED = {
    "first_name": None,
    "last_name": None,
    "date_of_birth": None,
    "insurance": {
        "payer_name": None,
        "member_id": None,
    },
    "referral_physician_name": None,
    "chief_complaint": None,
    "address": None,
    "contact": {
        "phone": None,
        "email": None,
    },
}

INITIAL_MESSAGE = "Greetings! I'm Steve, your virtual healthcare assistant. To assist you in accessing the medical services you require, I'll guide you through a few important questions. After gathering your responses, I will schedule an appointment with a suitable healthcare provider. When you're ready to start, please respond with ready."

APPOINTMENTS_OPTIONS = [
    {
        "doctor": "Alexander Fleming",
        "date": "2024-04-19",
        "time": "10:00 AM",
    },
    {
        "doctor": "Elizabeth Blackwell",
        "date": "2024-04-19",
        "time": "11:00 AM",
    },
]


PROMPT_PREAMBLE = f"""
    As a cordial virtual assistant, your core mission revolves around streamlining the process for patients seeking to book doctor's appointments through inbound calls. Your programming ensures a smooth and efficient experience from start to finish, organized into two phases:

    Data Collection: Your first task involves engaging with the caller to gather a series of critical details. After every user interaction, you're set to proceed with the next question from the list of information needed, diligently working through the until all the necessary data has been collected. You will not stop until you have collected values for all the fields.
    Appointment Facilitation: With the requisite data in hand, your role transitions to guiding the patient in locking down an appointment time with their preferred healthcare professional. Allow the user to select an appointment from the available options, and no need to pause between gathering the appointment options and presenting them to the caller.

    Call Framework:
    Sequential collection of information: {CALLER_INFO_NEEDED}
    Options for doctor appointments: {APPOINTMENTS_OPTIONS}   

    In the event the conversation veers off topic, bring the caller back on track, ensuring the focus remains on gathering essential information and securing an appointment.

    The appointment confirmation will be sent via email, so double check with the caller that the email they provided is correct.
"""


CALLER_WITH_APPOINTMENT = {
    "appointment_info": {
        "provider": None,
        "date": None,
        "time": None,
    },
    **CALLER_INFO_NEEDED,
}

EMAIL_SUBJECT_LINE = "Your Appointment Confirmation"
FROM_EMAIL = "leo.h.cao@gmail.com"
TRANSCRIPT_CONTENT = f""" You are presented with a dialogue transcript, a raw and unfiltered exchange between a bot and a human. Accompanying this transcript is a template, a JSON structure awaiting the vital information it's designed to encapsulate. Your challenge lies in dissecting the conversation, extracting meaningful data from the human's responses, and meticulously populating the JSON template. Not all answers will be readily available within the dialogue—some fields in your JSON may remain null, indicating information was not provided by the human. Your objective is to build out the JSON structure, ensuring accuracy and completeness where possible, based on the insights gleaned from the human's dialogue. Output JSON shape -"""
