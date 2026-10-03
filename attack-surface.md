# Attack Surface Map

This map is included as the portfolio documentation for the RAG target.

| Stage | What lives here | Security topic |
|---|---|---|
| Document store | PDF ingestion, chunks, embeddings, vector DB | Data / RAG poisoning |
| User question | Raw user-controlled text | Direct prompt injection / jailbreaks |
| Retrieved context | Text selected by similarity search | Indirect prompt injection |
| Model prompt | Question + retrieved context | Context manipulation |
| Final answer | Model output returned to user | Sensitive information disclosure |

## Why these boundaries matter

RAG does not retrain the model. Retrieved document text is placed into the model's context before generation. That makes the document store and retrieved content important security boundaries.

This repository is a learning target. Only test systems and documents you own or are explicitly authorized to test.


---
**Project by:** Hassan Ansari — [@trickyhash](https://instagram.com/trickyhash) · [@th3hash](https://github.com/th3hash)
