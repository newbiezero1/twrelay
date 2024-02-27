import requests

import config


def call_to_worker():
    url = "https://calling.api.sinch.com/calling/v1/callouts"
    payload="{\n  \"method\": \"ttsCallout\",\n  \"ttsCallout\": {\n    \"cli\": \"" + config.sinch_phone_from + "\",\n    \"domain\": \"pstn\",\n    \"destination\": {\n      \"type\": \"number\",\n      \"endpoint\": \""+ config.worker_phone +"\"\n    },\n    \"locale\": \"en-US\",\n    \"prompts\": \"#tts[wake up]\"\n  }\n}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic MTYyNTVlZjQtOWJmYy00ZmE1LWI3NWMtMDM0NWVhZDkzZWI3Om8yazVxK2dxcDBlWGE3Zng0WHhyUVE9PQ=='
    }
    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.json())
