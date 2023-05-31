import csv
import requests
from bs4 import BeautifulSoup

def get_video_duration(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    duration_tag = soup.find('span', {'class': 'ytp-time-duration'})
    if duration_tag:
        return duration_tag.text.strip()
    return None

def process_video_links(input_file, output_file):
    with open(input_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header if present
        with open(output_file, 'w', newline='') as output:
            writer = csv.writer(output)
            writer.writerow(['Link', 'Duration'])
            for row in reader:
                video_link = row[0]
                duration = get_video_duration(video_link)
                writer.writerow([video_link, duration])

# Usage
input_file = 'input.csv'
output_file = 'output.csv'
process_video_links(input_file, output_file)
