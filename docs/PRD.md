# Product Requirements Document (PRD)

## Project Name
Yojana Setu (योजना सेतु)

## Objective
To build an AI-powered government scheme discovery and eligibility assistant that helps citizens find and understand benefits they are eligible for.

## Problem Statement
Citizens often miss out on government schemes because:
1. Information is scattered across various government websites.
2. The language and eligibility criteria are complex and hard to decipher.
3. Search engines return generic or outdated lists rather than personalized recommendations.

## Solution
A web application where users can describe their situation in natural language and optionally provide profile details (age, income, state, etc.). The system dynamically searches for schemes, extracts current eligibility criteria, evaluates the user's profile against them, and presents clear, actionable results.

## Key Features
- **Natural Language Input**: Users can ask queries like "What schemes are available for a 20yo B.Tech student from UP?"
- **Dynamic Search Pipeline**: Uses Web Search APIs to pull real-time data from `.gov.in` and `.nic.in` domains.
- **LLM-Powered Extraction**: Transforms unstructured scheme text into structured JSON (conditions, benefits, steps).
- **Deterministic Eligibility**: Logic engine computes eligibility based on structured rules, avoiding LLM hallucinations.
- **Bilingual UI**: Available in English and Hindi.
- **Dark/Light Mode**: User preference based theme toggling.

## Constraints & Non-Goals
- We do not apply for schemes on behalf of the user.
- We do not store user data persistently (stateless search).
- We rely on the accuracy of the sources retrieved via search.
