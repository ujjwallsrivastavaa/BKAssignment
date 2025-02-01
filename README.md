# FAQ API

This project offers an API for managing and retrieving Frequently Asked Questions (FAQs) in multiple languages. It features automatic translation for multilingual support and caches responses for improved performance.

## Features

- **Retrieve FAQs in English**: By default, FAQs are provided in English if no language is specified.
- **Multilingual FAQ Support**: Users can request FAQs in any supported language. If a translation is unavailable in the database, it will be generated automatically.
- **Caching for Faster Responses**: Translated FAQs are cached to minimize repeated translation requests and enhance efficiency.
- **Dynamic Language Addition**: New languages can be added on the fly, with Google Translate handling missing translations.

## Requirements

- Python 3.x
- Django 3.x or later
- Django Rest Framework
- Googletrans (Google Translate API client)
- Redis 

## Installation

### Step 1: Clone the Repository

  ```bash
  git clone https://github.com/ujjwallsrivastavaa/BKAssignment
  cd BKAssignment
  ```
### Step 2: Set Up a Virtual Environment
On macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```
On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Navigate to the Server Directory

```bash
cd server
```

### Step 5: Apply Database Migrations
Run the migrations to set up the database:

```bash
python manage.py migrate
```

### Step 6: Start the Development Server

```bash
python manage.py runserver
```
The API will be available at http://127.0.0.1:8000.

## API Endpoints
### 1. Retrieve All FAQs
#### Request
```bash
http://127.0.0.1:8000/api/faqs/ 
```
Optional Query Parameter: lang – The language code (e.g., en, hi, bn). If omitted, English (en) is used as the default.

#### Response
- 2200 OK – Returns a list of FAQs. If a translation exists, it is provided; otherwise, the API generates one using Google Translate.
- If translation fails (e.g., due to API issues), English content is returned as a fallback.


  ```json
  [
      {
          "question": "What is Django?",
          "answer": "Django is a Python web framework."
      },
      {
          "question": "What is the purpose of this API?",
          "answer": "This API provides FAQ translation services."
      }
  ]
  ```
#### Language Fallback Mechanism:

If the requested language is missing, the API attempts translation via Google Translate. If unsuccessful, it defaults to English.

## Testing

The API can be tested using pytest, with coverage for:

- Fetching FAQs in English.
- Retrieving translated FAQs. (e.g., German).
- Handling invalid language codes.
- Model and database interactions, including save functions.

### Run Tests

```bash
pytest
```

