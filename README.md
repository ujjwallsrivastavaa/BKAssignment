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
  git clone https://github.com/ujjwallsrivastavaa/BharatFDAssignment
  cd BharatFDAssignment
  ```
### Step 2: Create and Activate a Virtual Environment
On macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```
On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Move to the server directory

```bash
cd server
```

### Step 5: Apply Database Migrations
Run the migrations to set up the database:

```bash
python manage.py migrate
```

### Step 6: Run the Development Server

```bash
python manage.py runserver
```
Your application will now be accessible at http://127.0.0.1:8000.

## API Endpoints
### 1. Get All FAQs
#### Request
```bash
http://127.0.0.1:8000/api/faqs/ 
```
Optional Query Parameter: lang – The language code (e.g., en, hi, bn). If not provided, the default language is English (en).

#### Response
- 200 OK – Returns a list of FAQs. If the requested language translation is available, it will return the translated FAQs. Otherwise, it will try to convert the FAQs to the requested language using Google Translate and return the translated content.
- If the requested language cannot be translated (e.g., due to a failed API call), the API will fall back to returning the FAQs in English.



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
#### Language Fallback Behavior:

If the requested language is not present in the database, the API will attempt to convert the FAQ content into the requested language using Google Translate. If the translation fails, the content will fall back to the default English language (i.e., en). In case of translation failure, the FAQ content will be returned in English.

## Testing

To test the API, you can use pytest. The project includes tests for the following cases:

- Retrieving FAQs in English.
- Retrieving FAQs in other languages (e.g., French).
- Retrieving FAQs with a nonexistent language code.
- Testing model behavior and database interactions. This includes testing save functions on the models.

### Run Tests

```bash
pytest
```

