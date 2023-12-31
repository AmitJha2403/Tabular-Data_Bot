# Box Office Data Explorer

This is a Python application that allows you to explore and interact with box office data from a Wikipedia page. You can view raw HTML data, structured data, filter data by date, and even ask questions about the box office data using a chat interface powered by OpenAI's GPT-3.5 model.

Here is the Google Drive Link for the Video description-
```
https://drive.google.com/drive/folders/1iHJ3x8bsvTfBpi5h3KYTyceNkimAJktI?usp=sharing
```

## Table of Contents

- [Getting Started](#getting-started)
- [Usage](#usage)
- [Features](#features)
- [Dependencies](#dependencies)
- [Configuration](#configuration)
- [License](#license)

## Getting Started

Follow these steps to get started with the Box Office Data Explorer:

1. Clone this repository to your local machine:

```bash
https://github.com/AmitJha2403/Tabular-Data_Bot.git
```

2. Navigate to the project directory:

```bash
cd Tabular-Data_Bot
```


3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project directory and add your OpenAI API key:
```bash
OPENAI_API_KEY=your_api_key_here
```

5. Run the Streamlit app:
```bash
streamlit run main.py
```

6. The app should now be running locally. Open a web browser and navigate to the URL provided by Streamlit to interact with the application.

## Usage

The Box Office Data Explorer provides several features:

- **Raw Data**: View the raw HTML data scraped from the Wikipedia page.
- **Structured Data**: View the parsed and structured box office data.
- **Filtered Data**: Filter the data by specifying a date range.
- **Chat with Data**: Ask questions about the box office data and receive answers generated by the OpenAI GPT-3.5 model.

## Features

### Raw Data

You can view the raw HTML data as it is scraped from the Wikipedia page. This can be useful for debugging and understanding the source of the box office data.

### Structured Data

The structured data represents the box office data in a more organized format. It includes film names, box office amounts, release dates, and any additional notes.

### Filtered Data

You can filter the data by specifying a date range. This allows you to narrow down the box office data to a specific time frame.

### Chat with Data

You can ask questions about the box office data using the chat interface. The application uses OpenAI's GPT-3.5 model to generate responses based on the structured data. Simply enter your question, and the model will provide relevant answers.

## Dependencies

The Box Office Data Explorer relies on the following Python libraries:

- Streamlit: For creating the web application interface.
- Requests: For making HTTP requests to scrape data.
- BeautifulSoup: For parsing HTML content.
- Pydantic: For data validation and modeling.
- OpenAI: For integrating the GPT-3.5 model.
- Dotenv: For loading environment variables from a .env file.

All dependencies are listed in the `requirements.txt` file and can be installed using `pip`.

## Configuration

To configure the application, you need to set up an environment variable for your OpenAI API key. Create a `.env` file in the project directory and add the following line:
```bash
OPENAI_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your actual OpenAI API key.

