import ollama
desiredModel = 'deepseek-r1:7b'
questionToAsk = 'How to solve a quadratic equation x^2+5*x+6=0'

response = ollama.chat(model=desiredModel, messages=[
    {
        'role': 'user',
        'content' : questionToAsk,
    },
])

OllamaResponse = response['message']['content']

print(OllamaResponse)

with open("OutputOllama.txt", "w", encoding="utf-8") as text_file:
     text_file.write(OllamaResponse)