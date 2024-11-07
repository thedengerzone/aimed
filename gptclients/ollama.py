#%%
import ollama


def generate_response(content):
    response = ollama.chat(model='llama3.2:1b', messages=[
        {
            'role': 'user',
            'content': content,
        },
    ])
    if 'message' in response and 'content' in response['message']:
        print(response['message']['content'])
    else:
        print("Unexpected response format:", response)
    return response

generate_response("What have you done")
#%%
