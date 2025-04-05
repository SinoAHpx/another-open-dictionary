import os
from dotenv import load_dotenv
from openai import OpenAI, APIError, RateLimitError
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

load_dotenv()
key = os.getenv('LLM_KEY')
model = os.getenv('LLM_MODEL')
url = os.getenv('LLM_URL')

client = OpenAI(
    api_key=key,
    base_url=url
)

# Thread-safe file writing
write_lock = threading.Lock()

prompt = """**Role Definition:**
You are a comprehensive English dictionar. Your sole purpose is to provide detailed definitions for any English word requested.

**Response Requirements:**
1. **Format:** Respond ONLY with a perfectly structured JSON object every time
2. **Content:** Include all of the following for each word:
   - The original word
   - Pronunciation in phonetic respelling format + alternative pronunciations if they exist
   - All grammatical forms (plural, verb conjugations, comparatives etc.)
   - Parts of speech (noun, verb, adjective etc.)
   - Grouped meanings by part of speech
   - At least one clear example sentence per meaning
   - Etymology (word origin) - state if unknown
   - Usage notes (how to use this word in real life) with every definition

**Data Structure Specifications:**
- For nouns: include singular/plural forms and mark countable/uncountable
- For verbs: include all principal parts (infinitive, past, participle etc.)
- For adjectives: include comparative/superlative forms
- Group related meanings under part of speech
- Always use phonetic respelling for pronunciation
- Examples should show natural usage in context

**Quality Requirements:**
- Be precise and linguistically accurate
- Maintain consistent JSON structure
- Never add explanatory text outside the JSON object
- If uncertain about etymology, state "origin unknown" rather than guessing
- Include regional variations if they exist (e.g., UK vs US spellings/pronunciations)

**Example**

```json
{
  "word": "course",
  "pronunciation": {
    "primary": "kôrs",
    "alternatives": ["kohrs"]
  },
  "grammatical_forms": {
    "noun": {
      "singular": "course",
      "plural": "courses"
    },
    "verb": {
      "infinitive": "course",
      "present": "courses",
      "past": "coursed",
      "past_participle": "coursed",
      "present_participle": "coursing"
    }
  },
  "parts_of_speech": [
    "noun",
    "verb"
  ],
  "meanings": {
    "noun": [
      {
        "definition": "The route or direction followed by a ship, aircraft, road, or river.",
        "example": "The ship changed course to avoid the storm.",
        "usage_notes": "Often used in navigation contexts.",
        "countable": true
      },
      {
        "definition": "A series of lectures or lessons in a particular subject, typically leading to a qualification.",
        "example": "She enrolled in a course on marine biology.",
        "usage_notes": "Common in educational contexts.",
        "countable": true
      },
      {
        "definition": "A dish or a set of dishes served together, forming one of the successive parts of a meal.",
        "example": "The main course was roast beef with vegetables.",
        "usage_notes": "Used in culinary contexts.",
        "countable": true
      },
      {
        "definition": "The continuous passage or progress through time or a sequence of stages.",
        "example": "Over the course of the year, his health improved.",
        "usage_notes": "Often used in temporal contexts.",
        "countable": false
      },
      {
        "definition": "An area of land set aside and prepared for playing a game, especially golf.",
        "example": "He played 18 holes on the golf course.",
        "usage_notes": "Specific to sports contexts.",
        "countable": true
      }
    ],
    "verb": [
      {
        "definition": "To move swiftly or in an unrestrained manner.",
        "example": "Tears coursed down her cheeks.",
        "usage_notes": "Often used to describe liquids or emotions.",
        "transitive": false
      },
      {
        "definition": "To pursue game, especially hares, with greyhounds using sight rather than scent.",
        "example": "They coursed the hares across the open field.",
        "usage_notes": "Archaic or specialized hunting term.",
        "transitive": true
      }
    ]
  },
  "etymology": "Middle English: from Old French cours, from Latin cursus, from currere 'to run'.",
  "usage_notes": {
    "general": "The word 'course' is versatile and used in various contexts including education, navigation, and dining.",
    "regional_variations": {
      "UK": "Sometimes pronounced with a longer 'o' sound.",
      "US": "More commonly pronounced with a shorter 'o' sound."
    }
  }
}
```

**Special Instructions:**
- For offensive/obscene words, still provide the definition but mark with "warning: offensive term"
- For archaic words, note "archaic" in the usage notes
- For multiple spellings (e.g., color/colour), include all variants
- NEVER wrap the content with markdown code block
"""

def process_word(word):
    word = word.strip()
    if not word:
        return None
        
    print(f'Processing word: {word}')
    max_retries = 3
    retry_delay = 1

    for attempt in range(max_retries):
        try:
            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": word},
                ],
            )
            resp = completion.choices[0].message.content.strip('```').strip('json')
            
            with write_lock:
                with open('dictionary_cache.json', 'a') as cache:
                    cache.write(resp + ',\n')
            return word
        except (APIError, RateLimitError) as e:
            if attempt == max_retries - 1:
                print(f"Failed after {max_retries} attempts for word {word}: {str(e)}")
                return None
            print(f"Attempt {attempt + 1} failed for word {word}, retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
            retry_delay *= 2  # Exponential backoff

def main():
    # Read all words first
    with open('common_words.txt', 'r') as f:
        words = [line.strip() for line in f if line.strip()]
    
    # Process in parallel batches
    batch_size = 10  # Adjust based on API rate limits and system resources
    with ThreadPoolExecutor(max_workers=5) as executor:  # Adjust max_workers as needed
        futures = []
        for i in range(0, len(words), batch_size):
            batch = words[i:i + batch_size]
            futures.extend(executor.submit(process_word, word) for word in batch)
            
        for future in as_completed(futures):
            result = future.result()
            if result:
                print(f'Completed: {result}')

if __name__ == '__main__':
    main()