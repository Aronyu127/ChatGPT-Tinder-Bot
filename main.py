import datetime
import os
import json
from src.chatgpt import ChatGPT, DALLE
from src.models import OpenAIModel
from src.tinder import TinderAPI
from src.dialog import Dialog
from src.logger import logger
from opencc import OpenCC

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
load_dotenv('.env')

models = OpenAIModel(api_key=os.getenv('OPENAI_API'), model_engine=os.getenv('OPENAI_MODEL_ENGINE'))

chatgpt = ChatGPT(models)
dalle = DALLE(models)
dialog = Dialog()
app = FastAPI()
scheduler = AsyncIOScheduler()
cc = OpenCC('s2t')
TINDER_TOKEN = os.getenv('TINDER_TOKEN')

def export_valuable_messages():
    tinder_api = TinderAPI(TINDER_TOKEN)
    profile = tinder_api.profile()
    user_id = profile.id
    for match in tinder_api.matches(limit=100):
        chatroom = tinder_api.get_messages(match.match_id)
        count = len(chatroom.messages)
        dialog.export_message_json(user_id, chatroom.messages[::-1]) if count > 20 else None
    combine_json_files(user_id)

def combine_json_files(user_id):
    file_path = f'chat_data/{user_id}'
    json_files = [file for file in os.listdir(file_path) if file.endswith('.json')]
    combined_data = []
    for file in json_files:
        with open(f'chat_data/{user_id}/{file}', 'r') as f:
            data = json.load(f)
            combined_data.append(data)
    with open(f'chat_data/{user_id}/combined.jsonl', 'w', encoding="utf-8") as f:
        for item in combined_data:
            json.dump(item, f, ensure_ascii=False)
            f.write('\n')


@scheduler.scheduled_job("cron", minute='*/5', second=0, id='reply_messages')
def reply_messages():
    tinder_api = TinderAPI(TINDER_TOKEN)
    profile = tinder_api.profile()
    interests = ', '.join(profile.user_interests)
    user_id = profile.id

    for match in tinder_api.matches(limit=50):
        chatroom = tinder_api.get_messages(match.match_id)
        lastest_message = chatroom.get_lastest_message()
        if lastest_message:
            if lastest_message.from_id == user_id:
                from_user_id = lastest_message.from_id
                to_user_id = lastest_message.to_id
                last_message = 'me'
            else:
                from_user_id = lastest_message.to_id
                to_user_id = lastest_message.from_id
                last_message = 'other'
            sent_date = lastest_message.sent_date
            if last_message == 'other' or (sent_date + datetime.timedelta(days=5)) < datetime.datetime.now():
                content = dialog.generate_input(from_user_id, to_user_id, chatroom.messages[::-1])
                response = chatgpt.get_response(profile.bio, interests ,content)
                if response:
                    response = cc.convert(response)
                    if response.startswith('[Sender]'):
                        chatroom.send(response[8:], from_user_id, to_user_id)
                    else:
                        chatroom.send(response, from_user_id, to_user_id)
                logger.info(f'Content: {content}, Reply: {response}')


@app.on_event("startup")
async def startup():
    scheduler.start()


@app.on_event("shutdown")
async def shutdown():
    scheduler.remove_job('reply_messages')


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run('main:app', host='0.0.0.0', port=8080)

# export_valuable_messages()