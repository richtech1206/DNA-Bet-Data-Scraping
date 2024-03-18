# DNA Bet Data Scraping and Logging

## Project Overview

This Python script automates the extraction of lottery result data from the DNA Bet website and logs it into a Google Sheets document. It utilizes Selenium, BeautifulSoup, and gspread libraries for web scraping and data management.

## Video Preview

![Project Image Overview](https://github.com/DevRex-0201/Project-Images/blob/main/Py-DNA-Bet-Data-Scraping.png)

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [License](#license)

## Features

- **Dynamic Data Extraction:** Navigate the DNA Bet website, extract relevant lottery result data, and store it in a Google Sheets document.

- **User Interaction:** Set the duration for data extraction using a Tkinter input dialog, providing flexibility in automation.

- **Error Handling:** Robust error-handling mechanisms, including retrying failed operations and logging in again when necessary.

## Requirements

Before running the script, ensure you have the following installed:

- Python 3.x
- [ChromeDriver](https://sites.google.com/chromium.org/driver/) (matching your Chrome browser version)
- Libraries: requests, selenium, gspread, oauth2client, beautifulsoup4

Install the required libraries using:

```bash
pip install requests selenium gspread oauth2client beautifulsoup4
```

## Installation

1. Clone the repository to your local machine:

```bash
git clone https://github.com/username/repository.git
```

2. Navigate to the project directory:

```bash
cd your-repository
```

## Configuration

1. Create a virtual environment (optional but recommended):

```bash
python -m venv venv
```

2. Activate the virtual environment:

- On Windows:

```bash
venv\Scripts\activate
```

- On macOS/Linux:

```bash
source venv/bin/activate
```

3. Install the required libraries:

```bash
pip install -r requirements.txt
```

4. Update the `.env` file with your Google Sheets credentials path:

```env
GOOGLE_SHEETS_CREDENTIALS_PATH=/path/to/your/credentials.json
```

## Usage

1. Run the script:

```bash
python main_script.py
```

2. Follow the prompts to set the duration and observe the script logging data into the Google Sheets document.
