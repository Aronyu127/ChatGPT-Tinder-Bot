from src.models import ModelInterface
from openai import OpenAI

class ChatGPT:
    def __init__(self, model: ModelInterface):
        self.model = model

    def get_response(self, interests: str, bio: str, text: str) -> str:
        messages = [{
            'role': 'system',
            'content': '''
                This chatbot will act on behalf of the user to chat with other girls on the dating app. The chatbot should follow these guidelines to ensure engaging and natural conversations:
                1. Keep the conversation light, natural, and not awkward.
                2. Infuse humor and fun into the conversation.
                3. Base the conversation on the user's initial provided basic information.
                4. End messages with questions to encourage ongoing dialogue.
                5. Respond based on previous chat history provided.
                6. The goal of the conversation is to explore the girl's interests and eventually invite her out.
                7. Translate the conversation to Traditional Chinese.

                User Information: 
                    - Bio: {bio}
                    - Interests: {interests}
                    - Constellation: Capricorn
            '''
        }, {
            'role': 'user', 'content': text
        }]
        response = self.model.chat_completion(messages)
        content = response['choices'][0]['message']['content']
        return content


class DALLE:
    def __init__(self, model: ModelInterface):
        self.model = model

    def generate(self, text: str) -> str:
        return self.model.image_generation(text)




## ChatGpt Assistant Test code ##

# client = OpenAI(
#   api_key="xxxxxxxx",
# )

# assistant = client.beta.assistants.create(
#   name="Math Tutor",
#   instructions="You are a master of flirting with girls, with a witty and humorous way of chatting. You're very good at playing psychological push-pull games with girls and always provide plenty of emotional value.",
#   model="gpt-4o",
# )


# thread = client.beta.threads.create(
#   messages=[
#     {
#         "role": "assistant",
#         "content": "👋"
#     },
#     {
#         "role": "user",
#         "content": "Heyy"
#     },
#     {
#         "role": "assistant",
#         "content": "週末在幹嘛呢"
#     },
#     {
#         "role": "user",
#         "content": "一天上班一天去綠島玩"
#     },
#     {
#         "role": "user",
#         "content": "你呢"
#     },
#     {
#         "role": "assistant",
#         "content": "！"
#     },
#     {
#         "role": "assistant",
#         "content": "綠島是可以只去一天的嗎"
#     },
#     {
#         "role": "assistant",
#         "content": "這麼厲害"
#     },
#     {
#         "role": "assistant",
#         "content": "我跟朋友去吃飯 看電影 酒吧小酌"
#     },
#     {
#         "role": "assistant",
#         "content": "踏青？"
#     },
#     {
#         "role": "user",
#         "content": "去了四天啦🤣🤣 去一天好狂哈哈哈"
#     },
#     {
#         "role": "user",
#         "content": "雖然我也是遇過去一天的"
#     },
#     {
#         "role": "user",
#         "content": "看哪部電影啊"
#     },
#     {
#         "role": "assistant",
#         "content": "我想說去一天應該一到就要回來了吧"
#     },
#     {
#         "role": "assistant",
#         "content": "😂"
#     },
#     {
#         "role": "assistant",
#         "content": "踩一下打個卡"
#     },
#     {
#         "role": "assistant",
#         "content": "就踏上歸途"
#     },
#     {
#         "role": "assistant",
#         "content": "哈哈哈哈"
#     },
#     {
#         "role": "assistant",
#         "content": "挺幽默"
#     },
#     {
#         "role": "assistant",
#         "content": "看瘋狂麥斯前傳"
#     },
#     {
#         "role": "assistant",
#         "content": "你有看過嗎"
#     },
#     {
#         "role": "assistant",
#         "content": "挺好看的"
#     },
#     {
#         "role": "assistant",
#         "content": "芙莉歐莎"
#     },
#     {
#         "role": "user",
#         "content": "台北去綠島舟車勞頓只待一天太可惜"
#     },
#     {
#         "role": "user",
#         "content": "有 那部好看！"
#     },
#     {
#         "role": "user",
#         "content": "雖然覺得電影有點太長🤣"
#     },
#     {
#         "role": "assistant",
#         "content": "真的挺好看的， 你最近還有看什麼其他電影嗎？"
#     }
#   ]
# )




# run = client.beta.threads.runs.create(
#   thread_id=thread.id,
#   assistant_id=assistant.id
# )

# run_steps = client.beta.threads.runs.steps.list(
#     thread_id=thread.id,
#     run_id=run.id
# )

# run_step = client.beta.threads.runs.steps.retrieve(
#     thread_id=thread.id,
#     run_id=run.id,
#     step_id="step_G8uuFZAgUOxTcag1VmtG7fLe"
# )

# thread = client.beta.threads.retrieve(thread.id)
# thread_messages = client.beta.threads.messages.list(thread.id, limit=40)

# for i in thread_messages.data:
#     print(i.content)