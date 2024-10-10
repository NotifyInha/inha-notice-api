from functools import wraps
import json
import os

import requests

class CompletionExecutor:
    def __init__(self, host, url, api_key, api_key_primary_val, request_id):
        self._url = url
        self._host = host
        self._api_key = api_key
        self._api_key_primary_val = api_key_primary_val
        self._request_id = request_id

    def execute(self, completion_request):
        headers = {
            'X-NCP-CLOVASTUDIO-API-KEY': self._api_key,
            'X-NCP-APIGW-API-KEY': self._api_key_primary_val,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id,
            'Content-Type': 'application/json; charset=utf-8',
        }

        with requests.post(self._host + self._url,
                        headers=headers, json=completion_request, stream=False) as r:
            res = r.json()
            if res['status']['code'] == '20000':
                return res['result']['message']['content']

            else:
                raise Exception(res['status']['message'])
            
            
def exception_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error in {func.__name__}: {str(e)}")
            return None
    return wrapper


@exception_handler
def naverapi(title, content):
    url = "https://naveropenapi.apigw.ntruss.com/text-summary/v1/summarize"
    headers = {
        "X-NCP-APIGW-API-KEY-ID": os.environ['NAVERID'],
        "X-NCP-APIGW-API-KEY": os.environ['NAVERSECRET'],
        "Content-Type": "application/json",
    }

    data = {
        "document": {
            "title": title,
            "content": content
        },
        "option": {
            "language": "ko",
            "model": "news",
            "tone": 2,
            "summaryCount": 3
        }
    }

    res = requests.post(url, headers=headers,
                        data=json.dumps(data).encode('utf-8'))
    resobj = json.loads(res.text)
    if res.status_code == 200:
        return resobj['summary']
    elif res.status_code == 401:
        raise Exception("api 인증 오류")
    elif res.status_code == 400:
        raise Exception(resobj['error']['errorCode'])
    else:
        raise Exception("알 수 없는 오류")

@exception_handler
def clova_ai_studio(title, content):
    completion_executor = CompletionExecutor(
        host='https://clovastudio.stream.ntruss.com',
        url='/testapp/v1/chat-completions/HCX-003',
        api_key=os.environ['CLOVAID'],
        api_key_primary_val=os.environ['CLOVASECRET'],
        request_id='a3e64c82-3782-4df4-8da2-a7087925d0c0'
    )

    request_data = json.loads(f"""{{
"messages": [
    {{"role":"system","content":"- 당신은 텍스트 요약 어시스턴트입니다.\\n- 주어진 텍스트를 분석하고 핵심 내용을 추출하여 간결하고 명확한 2줄 요약을 제공합니다."}},
    {{"role":"assistant","content":"제목 : {title}\\n내용 : {content}"}}
],
"topP": 0.6,
"topK": 0,
"maxTokens": 512,
"temperature": 0.1,
"repeatPenalty": 2.0,
"stopBefore": [],
"includeAiFilters": true,
"seed": 0
}}""", strict=False)

    response_text = completion_executor.execute(request_data)
    return response_text
