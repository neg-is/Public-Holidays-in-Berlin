from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests

def check_public_holiday(n):
    # URL to scrape public holidays
    URL = "https://publicholidays.de/berlin/2024-dates/"
    response = requests.get(URL)

    # Parse the page content
    web_page = response.text
    soup = BeautifulSoup(web_page, "html.parser")

    # Finding the correct table with public holidays
    holiday_table = soup.find("table", {"class": "publicholidays"})

    public_holidays = {}

    if holiday_table:
        rows = holiday_table.find_all("tr")

        # Extracting dates and descriptions from each row
        for row in rows:
            columns = row.find_all("td")
            if len(columns) >= 2:  # Check if the row has at least 2 columns (date and description)
                date_text = columns[0].get_text(strip=True) + " 2024"
                try:
                    # Parse and store the date
                    date = datetime.strptime(date_text, '%d %b %Y').strftime('%Y-%m-%d')
                    day = columns[1].get_text(strip=True)  # Fixed to use the correct column for day name
                    holiday = columns[2].get_text(strip=True)  # Fixed to use the correct column for holiday name
                    public_holidays[date] = holiday, day
                except ValueError:
                    print(f"Could not parse date: {date_text}")
                    continue

    else:
        print("No holiday table found.")
        return

    today = datetime.now()

    # Check for public holidays in the next 7 days
    holidays_found = False
    for i in range(1, n+1):
        next_date = today + timedelta(days=i)
        next_date_str = next_date.strftime('%Y-%m-%d')

        if next_date_str in public_holidays:
            print(f"{next_date_str} is a public holiday in Berlin: {public_holidays[next_date_str]}")
            holidays_found = True

        # if not holidays_found:
        #     print("No public holidays in the next 7 days.")

# Example usage
check_public_holiday(150)
