import streamlit as st
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, ValidationError
from typing import List, Dict, Optional
from datetime import datetime
import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Environment variables for OpenAI configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class BoxOfficeEntry(BaseModel):
    film_name: str
    box_office_amount: Optional[float]
    release_date: str
    notes: Optional[str]

def filter_by_date(data: List[Dict], start_date_str: str, end_date_str: str) -> List[Dict]:
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    filtered_data = []
    for entry in data:
        entry_date = datetime.strptime(entry['release_date'], "%B %d, %Y")
        if start_date <= entry_date <= end_date:
            filtered_data.append(entry)

    return filtered_data

def scrape_page_for_raw_text(url: str) -> str:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    target_table = soup.find('table', {'class': 'wikitable'})
    return str(target_table) if target_table else ''

def parse_html_to_structured_data(html_content: str) -> List[Dict]:
    soup = BeautifulSoup(html_content, 'html.parser')
    parsed_data = []
    table = soup.find('table', {'class': 'wikitable'})

    if not table:
        return parsed_data

    rows = table.find_all('tr')[1:]  # Skipping the header row

    for row in rows:
        columns = row.find_all('td')
        if not columns:
            continue

        weekend_end_date = columns[1].get_text(strip=True)
        film_name = columns[2].get_text(strip=True)
        gross_amount = columns[3].get_text(strip=True).replace('$', '').replace(',', '')
        notes = columns[4].get_text(strip=True) if len(columns) > 4 else None

        try:
            box_office_amount = float(gross_amount) if gross_amount else None
            film_data = BoxOfficeEntry(
                film_name=film_name,
                box_office_amount=box_office_amount,
                release_date=weekend_end_date,
                notes=notes
            )
            parsed_data.append(film_data.dict())
        except (ValueError, ValidationError):
            continue

    return parsed_data

def format_data_for_chat(structured_data):
    formatted_text = ""
    for entry in structured_data:
        notes = f" Notes: {entry['notes']}" if entry['notes'] else ""
        formatted_text += f"Film: {entry['film_name']}, Box Office: ${entry['box_office_amount']}, Release Date: {entry['release_date']}{notes}\n"
    return formatted_text

# Main processing logic updated for Streamlit
def main():
    st.title('Box Office Data Explorer')

    url = "https://en.wikipedia.org/wiki/List_of_2023_box_office_number-one_films_in_the_United_States"
    raw_text = scrape_page_for_raw_text(url)
    structured_data = parse_html_to_structured_data(raw_text)

    # Dropdown to choose what to view, including chat option
    view_option = st.selectbox("Choose data to view", ["Raw Data", "Structured Data", "Filtered Data", "Chat with Data"])
    
    if view_option == "Raw Data":
        st.subheader('Raw HTML Data')
        st.text(raw_text)
    elif view_option == "Structured Data":
        st.subheader('Structured Data')
        st.write(structured_data)
    elif view_option == "Filtered Data":
        # Date Filter on Main Page
        st.header("Filter by Date")
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", value=datetime(2023, 1, 1), min_value=datetime(2023, 1, 1), max_value=datetime(2023, 12, 31))
        with col2:
            end_date = st.date_input("End Date", value=datetime(2023, 12, 31), min_value=datetime(2023, 1, 1), max_value=datetime(2023, 12, 31))
        filtered_data = filter_by_date(structured_data, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
        st.subheader('Filtered Data')
        st.write(filtered_data)
    elif view_option == "Chat with Data":
        st.subheader('Chat with Data')
        formatted_structured_data = format_data_for_chat(structured_data)

        user_input = st.text_input("Ask a question about the box office data")
        if user_input:
            # openai.api_key = OPENAI_API_KEY
            openai.api_key = OPENAI_API_KEY
            full_prompt = f"{formatted_structured_data}\nQ: {user_input}\nA:"
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-1106",
                messages=[{"role": "system", "content": full_prompt}]
            )
            if response.choices:
                st.write(response.choices[0].message['content'])

if __name__ == "__main__":
    main()
