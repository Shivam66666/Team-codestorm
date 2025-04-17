
from groq import Groq
from json import dump , load
import datetime
from dotenv import dotenv_values
import os
current_dir =( os.path.dirname(__file__) + '\\')
env_vars = dotenv_values(rf"{current_dir}.env")


groqapikey = env_vars.get("grokdikey")


client = Groq(api_key = groqapikey)

messages = []

System = f"""Hello  You are a very accurate and advanced AI-Generated Insights provider
*** Reply in only English***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""



systemchatbot = [
    {"role":"system" , "content" : System}
]





def chatbot(query):
    try :


        messages.append({"role":"user" , "content" : f"{query}"})

        completion = client.chat.completions.create(
            model = "llama3-70b-8192",
            messages = systemchatbot + messages ,
            # max_token =  1024,
            temperature = 0.7,
            top_p = 1,
            stream = True,
            stop = None 
        )

        answer = ""

        for chunk in completion:
            if chunk.choices[0].delta.content:
                answer += chunk.choices[0].delta.content

        answer = answer.replace("</s>","")

        messages.append({"role": "assistant" , "content" : answer}) 



        return (answer)
    except Exception as e:
        print(f"error :{e}")

        return chatbot(query)


if __name__ == "__main__":
    while True:
        user_inp = input(">>")
        print(chatbot(user_inp))

