# System Architecture

## Overview
Yojana Setu is designed as a modular, stateless, service-oriented monolith. It separates the orchestration of external calls (Search, LLM) from the core business logic (Eligibility Engine).

## Tech Stack
- **Frontend**: React (Vite), JavaScript, Tailwind CSS v4
- **Backend**: Python 3.10+, FastAPI, Pydantic
- **Search Provider**: Strategy pattern supporting Tavily and Serper.
- **LLM Provider**: Strategy pattern supporting OpenAI, OpenRouter, and Google AI.

## Workflow (The Orchestrator Pipeline)

1. **Query Understanding**:
   - The user query is sent to the LLM to understand intent and extract implicit profile traits.
   - Outputs an optimized search query.

2. **Web Search**:
   - The Search Service uses the optimized query to fetch real-time web results.
   - Prioritizes `.gov.in` and official domains.

3. **Scheme Extraction**:
   - The LLM processes the retrieved text snippets.
   - Extracts structured scheme data: Name, Benefits, Eligibility Conditions (Age, Income, etc.), Documents, and Steps.

4. **Eligibility Evaluation**:
   - A deterministic, rule-based engine (`EligibilityEngine`) compares the extracted conditions against the combined user profile (explicit + implicit).
   - Assigns a status: `LIKELY_ELIGIBLE`, `POSSIBLY_ELIGIBLE`, `NEEDS_MORE_INFORMATION`, `LIKELY_NOT_ELIGIBLE`, or `UNVERIFIED`.

5. **Answer Generation**:
   - The LLM generates a final, user-friendly summary of the findings in the user's requested language.

## Architecture Diagram (Mental Model)

```
[ Frontend (React/Vite) ]
          |
    (REST API via FastAPI)
          |
[ Backend / Orchestrator ]
    /      |      \
[ LLM ] [Search] [Engine]
```
