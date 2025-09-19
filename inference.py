import ollama

response = ollama.chat(model="deepseek_finetuned_model",
            messages=[{ "role": "user", "content": "I wanna plan an Industrial Visit with as a part of our engineering college"
            },
                      ])

print(response.message.content)