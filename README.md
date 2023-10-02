# Employ Business Rating System

Get an overall ranking score for a business from various resources in one place
## Overview

The Employ Rating System is a Flask-based web application designed to calculate and display the overall rating of businesses based on various data points. The application fetches ratings from multiple sources like Yelp, Google Places, and BBB, and calculates a weighted average to provide an overall score for a business.

![Employ Logo](./images/employ.png)


## Features

- **User Interface**: A web-based UI that allows users to input business details and view the calculated ratings.
- **Configurable Weights**: Users can configure the weightage given to each rating source.
- **Log Management**: The application logs all the rating details and API responses for debugging and transparency.
- **Data Persistence**: Uses YAML files to store configuration settings.
- **Downloadable Logs**: Users can download the log files for offline analysis.

## Installation
Winodws or Linux
### Prerequisites

- Python 3.x
- Docker (optional)
- Conda (optional for environment management)

### Local Setup

#### Using Python's built-in venv

1. Clone the repository
```bash
git clone https://github.com/bigsk1/employ.git
```
2. Navigate to the project directory
```bash
cd employ
```
3. Create a virtual environment
```bash
python -m venv .venv
```
4. Activate the virtual environment
- On Windows:
 ```bash
.venv\Scripts\activate
```
- On macOS and Linux:

 ```bash
source .venv/bin/activate
```
5. Install required packages
```bash
pip install -r requirements.txt
```
6. Run the application
```bash
python app.py
```
#### You can also run from CLI python main.py and get output in terminal

#### Using Conda

1. Install [Conda](https://docs.anaconda.com/anaconda/install/) if you haven't already.
2. Create a new Conda environment
    ```bash
    conda create -n employ python=3.11.0
    ```
3. Activate the Conda environment
    ```bash
    conda activate employ
    ```
4. Follow steps 1, 2, 5, and 6 from the "Using Python's built-in venv" section.

### Docker

1. Docker image
```bash
docker pull bigsk1/employ:latest
```

2. Use the provided `docker-compose.yml` file to start the container.
 ```bash
docker-compose up
```
OR

3. Use a docker run command instead, add additional -e as needed
```bash
docker run --restart=always -p 5000:5000 -e YELP_API_KEY=yourkey bigsk1/employ:latest
``` 
visit localhost:5000
## Usage

1. Open your web browser and navigate to `http://localhost:5000`.
2. Input the business details and configure the weights for each rating source.
3. Click the "Run" button to fetch the ratings and calculate the overall score.

## Environment Variables

The application uses the following environment variables for API access:

- `YELP_API_KEY`
- `GOOGLE_API_KEY`
- `BBB_API_TOKEN`

These can be set in a `.env` file in the project directory.

You need to sign up and get the API keys and tokens to use the those options
## Contributing

Feel free to open issues or submit pull requests.
