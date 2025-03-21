import os
from dotenv import load_dotenv
from openai import AzureOpenAI  

load_dotenv()

endpoint = os.getenv("ENDPOINT_URL", "https://openaillmdemo93.openai.azure.com/")  
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-35-turbo")  
subscription_key = os.getenv("OPENAI_API_KEY")  

client = AzureOpenAI(  
    azure_endpoint=endpoint,  
    api_key=subscription_key,  
    api_version="2024-05-01-preview",
)
def ai_chat(user_message):
    message_text = [
       {"role":"system","content":"You are an AI assistant that helps people find information."},
       {"role": "user", "content": user_message}
    ]

    completion = client.chat.completions.create(  
        model=deployment,
        messages=message_text,
        max_tokens=400,  
        temperature=0.7,  
        top_p=0.95,  
        frequency_penalty=0,  
        presence_penalty=0,
        stop=None,  
        stream=False
    )
    return completion


print("Welcome! how can I help you today?")

while True:
    user_message = input(">> ")
    completion = ai_chat(user_message)
    # Completion will return a response that we need to use to get the acctual string
    print(completion.choices[0].message.content)