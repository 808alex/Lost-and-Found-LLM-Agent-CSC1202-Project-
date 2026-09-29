# 🔍 DCU Lost & Found Agent

An LLM-based agent that helps DCU students find their stuff — built for CSC1202.

![Django](https://img.shields.io/badge/Django-green?logo=django&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-blue?logo=mysql&logoColor=white)
![Status](https://img.shields.io/badge/status-in%20development-yellow)

## What it does

- **Found something?** Describe it + upload a photo — the agent extracts object, colour, brand, location and features automatically.
- **Lost something?** Describe it in your own words — the agent semantically matches it against everything logged as found.

```mermaid
flowchart LR
    A[Found item] -->|description + photo| B{{LLM Agent}}
    B -->|extracts attributes| C[(Database)]
    D[Lost item] -->|description| B
    C -->|ranked matches| D
```

## Stack

Django · MySQL · LLM API (TBD) · Bootstrap or React (TBD)

## Team

| Name | Role |
|---|---|
| Alexander Zudins | |

## Docs

- [`docs/deliverables/`](docs/deliverables/) — the three assessed reports
- [`docs/meeting-notes/`](docs/meeting-notes/) — meeting reports

---
CSC1202 · Prompt Engineering and LLM-Based Agents · DCU 2026
