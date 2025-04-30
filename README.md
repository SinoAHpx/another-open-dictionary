# Open Dictionary

This is another open dictionary which 20000+ words, which roughly covered COCA. 

- Powered by DeepSeek V3 (and this consumed about 45M tokens)
- Natrual pronounciation instead of IPA
- English definitions with ~~vivid~~ examples
- Part of speech, usage note, etymology and more

## Sample

```json
{
    "word": "open",
    "pronunciation": {
      "primary": "OH-puhn",
      "alternatives": []
    },
    "grammatical_forms": {
      "adjective": {
        "positive": "open",
        "comparative": "more open",
        "superlative": "most open"
      },
      "verb": {
        "infinitive": "open",
        "present": "opens",
        "past": "opened",
        "past_participle": "opened",
        "present_participle": "opening"
      },
      "noun": {
        "singular": "open",
        "plural": "opens"
      }
    },
    "parts_of_speech": ["adjective", "verb", "noun"],
    "meanings": {
      "adjective": [
        {
          "definition": "Not closed or barred; allowing access.",
          "example": "The door was left open all night.",
          "usage_notes": "Commonly used to describe physical objects like doors, windows, or containers.",
          "countable": false
        },
        {
          "definition": "Not covered or protected; exposed.",
          "example": "The wound was left open to the air.",
          "usage_notes": "Often used in medical or environmental contexts.",
          "countable": false
        },
        {
          "definition": "Available for use or participation.",
          "example": "The job position is still open.",
          "usage_notes": "Frequently used in professional or organizational settings.",
          "countable": false
        },
        {
          "definition": "Honest and not secretive.",
          "example": "She was very open about her feelings.",
          "usage_notes": "Used to describe people's attitudes or behaviors.",
          "countable": false
        },
        {
          "definition": "Not decided or settled.",
          "example": "The question is still open for debate.",
          "usage_notes": "Common in discussions or legal contexts.",
          "countable": false
        }
      ],
      "verb": [
        {
          "definition": "To move or adjust something so that it is no longer closed.",
          "example": "He opened the window to let in some fresh air.",
          "usage_notes": "Can be used both transitively and intransitively.",
          "transitive": true
        },
        {
          "definition": "To start or begin something.",
          "example": "The new store will open next month.",
          "usage_notes": "Often used for businesses, events, or ceremonies.",
          "transitive": false
        },
        {
          "definition": "To make accessible or available.",
          "example": "The government opened the borders to refugees.",
          "usage_notes": "Common in political or social contexts.",
          "transitive": true
        },
        {
          "definition": "To spread out or unfold.",
          "example": "She opened the map on the table.",
          "usage_notes": "Used for objects that can be expanded or unfolded.",
          "transitive": true
        }
      ],
      "noun": [
        {
          "definition": "A competition or tournament that is open to all participants.",
          "example": "He won the tennis open last year.",
          "usage_notes": "Primarily used in sports contexts.",
          "countable": true
        },
        {
          "definition": "The outdoors or a wide, unobstructed space.",
          "example": "They love to camp in the open.",
          "usage_notes": "Often poetic or literary usage.",
          "countable": false
        },
        {
          "definition": "A clear or obvious fact or situation.",
          "example": "The truth is now out in the open.",
          "usage_notes": "Used in idiomatic expressions.",
          "countable": false
        }
      ]
    },
    "etymology": "Old English 'open', of Germanic origin; related to Dutch 'open' and German 'offen', from an Indo-European root shared by Sanskrit 'apna' 'open' and Latin 'aperire' 'to open'.",
    "usage_notes": {
      "general": "The word 'open' is highly versatile and used in numerous contexts, from physical descriptions to abstract concepts.",
      "regional_variations": {
        "UK": "No significant variations.",
        "US": "No significant variations."
      }
    }
  }
```

### How to use

Yeah I know a json file with over 1 million lines is crazy, but there's no a mongodb lite for this kind object storage, and don't you think it is crazier to use sql databases to store raw json objects?

Guess I'll make a sql version too.

Just load this HUGE json into your memory, and here you go with your on-the-fly dictionary query.