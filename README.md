# CivicFix AI

**From Problem to Verified Action**

CivicFix AI is a civic-research prototype that helps citizens investigate local public issues, discover potentially relevant official complaint channels, and prepare a structured complaint draft.

## The Problem

Citizens may not know which authority to contact or where to find reliable information about a civic issue.

## How It Works

1. The user enters a civic issue and location.
2. SerpApi Google Search retrieves web research results.
3. SerpApi Google Maps retrieves location-related results.
4. SerpApi Google News retrieves relevant news results.
5. CivicFix filters potential official sources and suggests a possible authority.
6. It presents potential complaint channels and generates a complaint draft.

## Technology

- Python
- Flask
- SerpApi Python client
- Google Search, Google Maps and Google News engines
- python-dotenv

## Setup

1. Install Python 3.11 or later.
2. Clone this repository and enter its directory.
3. Create and activate a virtual environment.
4. Install dependencies:

   `pip install -r requirements.txt`

5. Create a `.env` file containing:

   `SERPAPI_KEY=PASTE_YOUR_KEY_LOCALLY`

6. Start the application:

   `python app.py`

7. Open `http://127.0.0.1:8501` in your browser.

## SerpApi Usage

CivicFix uses live search results from Google Search, Google Maps and Google News to gather different kinds of evidence related to a reported civic issue. These results inform the research workflow; they do not automatically prove that a source is relevant or that a particular authority is responsible.

## Limitations

- Authority matching is currently keyword-based and preliminary.
- Official-domain filtering does not guarantee that a page accepts a specific complaint.
- Road ownership and jurisdiction must be independently confirmed.
- Search results can be incomplete, outdated or irrelevant.
- This prototype does not submit complaints automatically.

## Security

Never commit your `.env` file, API keys or other secrets. Keep `.env` excluded through `.gitignore`.

## AI Tool Disclosure

AI assistance was used during project development. Update this section to accurately disclose the specific tools used and how they contributed before submission.

## Project Status

Hackathon prototype under active development.
