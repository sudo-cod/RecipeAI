from openai import OpenAI
import json
import time
from typing import List, Dict
from tqdm import tqdm


# =========================
# Generator
# =========================

class SyntheticDataGenerator:
    def __init__(self, api_key: str):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )

    def generate_structured_recipe(self, transcript: str) -> str:
        """Generate structured recipe from transcript"""

        prompt = f"""
Convert the following cooking video transcript into a clean, well-structured recipe.

Follow this EXACT format:

**RECIPE NAME**

**Ingredients:**
* Ingredient with precise measurement
* Ingredient with precise measurement

**Instructions:**
1. Step in chronological order
2. Step in chronological order

**Tips:**
- Tip if mentioned

Rules:
- Standardize measurements
- Infer reasonable quantities when missing
- Remove all promotions and filler speech
- Include temperatures and times if mentioned
- Preserve techniques and chef tips

Transcript:
{transcript}
"""

        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert chef and dataset curator."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_tokens=1000
        )

        return response.choices[0].message.content.strip()

    def convert_to_llama_format(self, dataset: List[Dict]) -> List[Dict]:
        output = []

        instruction = "Convert this cooking video transcript into a structured recipe."

        for item in dataset:
            output.append({
                "instruction": instruction,
                "input": item["transcript"],
                "output": item["structured_recipe"]
            })

        return output



def load_transcripts(path: str) -> List[Dict]:
    data = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            video_id, transcript = next(iter(obj.items()))
            data.append({
                "video_id": video_id,
                "transcript": transcript
            })
    return data


API_KEY = ""
INPUT_PATH = "transcript.jsonl"
OUTPUT_PATH = "recipe_dataset.jsonl"

generator = SyntheticDataGenerator(API_KEY)
transcripts = load_transcripts(INPUT_PATH)

dataset = []

for item in tqdm(transcripts):
    try:
        recipe = generator.generate_structured_recipe(item["transcript"])

        dataset.append({
            "video_id": item["video_id"],
            "transcript": item["transcript"],
            "structured_recipe": recipe,
            "recipe_type": "video_recipe"
        })

        time.sleep(1.2)  

    except Exception as e:
        print(f"[ERROR] {item['video_id']}: {e}")
        time.sleep(3)

formatted = generator.convert_to_llama_format(dataset)

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    for item in formatted:
        json.dump(item, f, ensure_ascii=False)
        f.write("\n")
