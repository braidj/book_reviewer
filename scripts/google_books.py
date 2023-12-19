import requests
from dotenv import load_dotenv
import os

load_dotenv("../dev.env")

# Get API key from environment variable
api_key = os.getenv('GOOGLE_BOOKS_API_KEY')

def get_book_genre(book_title):
    # Replace YOUR_API_KEY with your actual Google Books API key
    base_url = "https://www.googleapis.com/books/v1/volumes"

    # Prepare the query parameters
    params = {
        'q': book_title,
        'key': api_key
    }

    # Make the request
    response = requests.get(base_url, params=params)
    data = response.json()

    # Extract genre information
    if 'items' in data:
        for item in data['items']:
            volume_info = item.get('volumeInfo', {})
            categories = volume_info.get('categories', [])
            if categories:
                return categories  # Return the first category as the genre

    return "Genre not found"

# Example usage
book_title = "Dune"
genre = get_book_genre(book_title)
print(f"The genre of '{book_title}' is: {genre}")
