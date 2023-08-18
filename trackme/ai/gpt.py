import os
import pickle
import openai
from trackme.constants import OPEN_API_KEY

openai.api_key = OPEN_API_KEY

LOCATION_INTENT = 'location'
OTHER_INTENT = 'else'
NONE_TARGET = 'none'

samples = pickle.load(open(os.path.join(os.path.dirname(__file__), 'samples.pkl'), 'rb'))

SYSTEM_PROMPT = [
    {
        'role':
        'system',
        'content':
        f'You help a chatbot understand chat messages in casual Indonesian mixed with Javanese. Identify the intent of a message as \"{LOCATION_INTENT}\" if it asks anything related to location whereabouts and everything else as \"{OTHER_INTENT}\". Target is who the message is for, or \"{NONE_TARGET}\" if unknown. There can be more than one target. Respond with \"<intent>,<target_1>,<target_2>,...,<target_n>\". You will frequently receive the word \"ge\" or \"gek\" in the message. Those words mean \"sedang\" and are not target.'
    },
    *samples,
]


def extract_intent(content: str):
    try:
        messages = [*SYSTEM_PROMPT, {'role': 'user', 'content': f'{content}'}]
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=messages,
            temperature=0.3,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        result = response.choices[0]['message']['content'].split(',')
        if len(result) < 2:
            return None
        return result
    except:
        return None
