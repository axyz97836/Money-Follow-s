# API Reference

## Base URL
`/api`

## Endpoints

### 1. Health Check
`GET /health`

Returns the health status of the API and configured external services.

**Response (200 OK)**
```json
{
  "status": "ok",
  "version": "1.0.0",
  "environment": "development",
  "services": {
    "llm": "configured",
    "search": "configured"
  }
}
```

### 2. Search Schemes
`POST /search`

Initiates the full discovery and evaluation pipeline.

**Request**
```json
{
  "query": "I am a farmer from UP. Any schemes?",
  "profile": {
    "age": 45,
    "state": "Uttar Pradesh",
    "occupation": "Farmer"
  },
  "session_id": "optional-uuid"
}
```

**Response (200 OK)**
```json
{
  "query": "I am a farmer from UP. Any schemes?",
  "summary": "Here are some schemes that might help you...",
  "schemes": [
    {
      "name": "PM Kisan Samman Nidhi",
      "status": "LIKELY_ELIGIBLE",
      "description": "...",
      "benefits": [...],
      "why_it_matches": ["You are a farmer in Uttar Pradesh"],
      ...
    }
  ],
  "disclaimer": "...",
  "search_metadata": {
    "sources_checked": 5,
    "official_sources": 3
  },
  "session_id": "uuid-for-followup"
}
```

### 3. Follow-up Chat
`POST /chat`

Context-aware follow-up queries based on the initial search.

**Request**
```json
{
  "message": "What documents do I need for the first one?",
  "session_id": "uuid-from-search",
  "profile": {}
}
```

**Response (200 OK)**
Same format as `/search`.
