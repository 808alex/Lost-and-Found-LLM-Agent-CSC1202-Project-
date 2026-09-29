# agent/

The actual LLM agent code — kept separate from items/ deliberately, since
this is the part the module is graded on, and it shouldn't get buried
inside Django views.

Likely contents:
- `extraction.py` — turns a free-text description (+ photo) into
  structured attributes: object, colour, brand, location, features
- `matching.py` — semantic similarity between a lost description and
  stored found items
- `client.py` — the LLM API call wrapper, whichever provider you pick

Anticipates `python manage.py startapp agent` from inside backend/.

## prompts/

Prompt templates as their own files, not strings buried in code — this
is literally what the Week 3 slides recommend ("prompts can be managed
like code: stored as templates, versioned, tested and reused"). One file
per prompt, e.g. `extract_attributes.txt`, `match_similarity.txt`. Makes
prompt changes easy to diff across commits — useful evidence for the
"significant changes from the initial specification" section of the
Week 11 report.
