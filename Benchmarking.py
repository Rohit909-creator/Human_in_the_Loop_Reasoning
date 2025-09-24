# To run this code you need to install the following dependencies:
# pip install google-genai

import base64
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import json
from datasets import load_dataset
load_dotenv()

# Login using e.g. `huggingface-cli login` to access this dataset
ds = load_dataset("google/reveal", cache_dir="./benchmark_data")

# Suppose you have a list of dicts
# data = [
#     {"user_query": "What is 2+2?", "answer": 4},
#     {"user_query": "Capital of France?", "answer": "Paris"},
#     {"user_query": "Is fire hot?", "answer": True}
# ]

# Save as .jsonl
# with open("output.jsonl", "w", encoding="utf-8") as f:
#     for item in data:
#         f.write(json.dumps(item) + "\n")

def generate(sample):
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=sample),
                # types.Part.from_text(text="""INSERT_INPUT_HERE"""),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="application/json",
        system_instruction=[
            types.Part.from_text(text="""You are a data modifier for creating reasoning + clarification training data.

**Task:**
Given an original `Question` and `Answer`, rewrite them into a JSON object with the following rules:

1. **Modify the Question** so it is *incomplete*, ambiguous, or missing necessary details.
2. **Rewrite the Answer** into a **reasoning trace** with step-by-step thought.

   * Insert `<ask> … </ask>`, `<question> … </question>`, or `<doubt> … </doubt>` tokens when ambiguity or missing info arises.
   * After each token, simulate a **plausible user reply** in parentheses, e.g. `(User responds: …)`.
   * Incorporate the reply into the reasoning and continue until reaching the **final answer**.
3. Extract each **user reply** and store it as a list in `"clarifications"`.
4. Output the result strictly in JSON format:

```json
{
  "question": "…",
  "full_answer": "…",
  "clarifications": ["...", "..."]
}
```

---

### 🔹 Example Transformation

**Input:**

```
Question:
Suppose a meteor made of nickel and iron falls to the earth from deep space. Estimate how much its temperature would rise on impact ignoring any atmospheric effects.
Answer:
The temperature of the meteor would rise by a factor of 1.414 as nickel has a higher melting point. So the final answer is: 1.414
```

**Output JSON:**

```json
{
  "question": "Estimate the temperature rise of a meteor hitting Earth.",
  "full_answer": "To estimate the temperature rise, I need to know the initial velocity of the meteor upon impact. <ask> what kind of meteor is it, what is its composition? </ask> (User responds: Its nickel-iron.) Assuming equal parts nickel and iron, the temperature rise is proportional to a factor of 1.414 due to nickel's higher melting point, so the final answer is 1.414.",
  "clarifications": [
    "Assume 11 km/s.",
    "Iron: 450 J/kg·K, Nickel: 480 J/kg·K."
  ]
}
```
As you can see the augmentation done here, is based on the info available only based on the Question and Answer Data provided."""),
        ],
    )

    response = ""

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        # print(chunk.text, end="")
        response += chunk.text
        
    print(f"Response: {response}")
    obj = json.loads(response)
    print(f"Object: {obj}")
    
    # with open('Data2.jsonl', 'a', encoding="utf-8") as f:
    #     for data in obj:
    #         s = json.dumps(data)
    #         f.write(s+"\n")
            
    return response


if __name__ == "__main__":
    import time
    import random
    
    i = 16  
    # print(ds['eval'][i].keys())
    # print(ds['eval'][i]['correctness_label'])
    print("Question:")
    print(ds['eval'][i]['question'])
    print("Answer:")
    print(ds['eval'][i]['full_answer'])
    # n = len(ds['eval'])
    # num_trues = [ds['eval'][i]['correctness_label'] for i in range(n)]
    # print(f"Total Number of correct: {num_trues.count('Correct')}/{n}")
    # print(num_trues.index('Correct', i+1))
    print('\n\n')
    generate(ds['eval'][i]['question']+"\n"+ds['eval'][i]['full_answer'])
    
    # while True:
        # print(generate())
        # delay = random.randint(0, 5)
        # print(f"waiting: {delay}")
        # time.sleep(delay)