import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys
from media_extractor import MediaLocator


def get_book_genres(book_title, author_name):
    # Format the book title and author name for URL encoding
    formatted_title = '+'.join(book_title.split())
    formatted_author = '+'.join(author_name.split())

    # The URL for Goodreads search (might need to be updated based on the website structure)
    search_url = f"https://www.goodreads.com/search?q={formatted_title}+{formatted_author}"

    try:
        response = requests.get(search_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the first search result link (modify this based on actual page structure)
        book_link = soup.find('a', class_='bookTitle')['href']

        # Fetch the book page
        book_page_response = requests.get(f"https://www.goodreads.com{book_link}")
        book_page_response.raise_for_status()

        book_soup = BeautifulSoup(book_page_response.content, 'html.parser')

        # Extract the genres from the specified section
        genres_list = book_soup.find('div', {'data-testid': 'genresList'})
        genres = [genre.text.strip() for genre in genres_list.find_all('span', class_='Button__labelItem')]

        return genres if genres else ["Genre not found"]

    except requests.RequestException as e:
        return [f"An error occurred: {e}"]
    except (AttributeError, TypeError):
        return ["Genre not found or parsing error."]

def lookup_title_author(book_title, author_name):
    """Lookup the book title and author name on Goodreads and return the joined genres."""

    genres = get_book_genres(book_title, author_name)
    result = ' '.join(genres)
    print(f"{book_title} by {author_name}: {result}")
    return result

def get_book_genres(batch_size=1000):

    file_path = "D:/OneDrive/Books/five star books.csv"
    df = pd.read_csv(file_path, encoding='utf-8')
    genres_ix = df.columns.get_loc('Genres')

    counter = 0
    for i in range(len(df)):

        if counter < batch_size and pd.isnull(df.iloc[i, genres_ix]):
            df.at[i,"Genres"] = lookup_title_author(df.loc[i,"Title"], df.loc[i,"Authors"])
            df.to_csv(file_path, index=False, encoding='utf-8')
            counter += 1
            if counter % 10 == 0:
                print(f"{counter} out of {batch_size} books processed.")
def get_selected_books(col_name, col_value):
    """Get the list of books that match the specified column value."""
    file_path = "D:/OneDrive/Books/five star books.csv"
    df = pd.read_csv(file_path, encoding='utf-8')
    return df[df[col_name] == col_value]
def main():

    media_locator = MediaLocator(r"\\MYCLOUDEX2ULTRA\Public\Books\5Start list\MOBI",r"\\MYCLOUDEX2ULTRA\Public\Books\pending transfer\Ben")
    books = get_selected_books("Ben", "Y")

    for i in range(len(books)):
        media = media_locator.get_media(books.iloc[i, 0],books.iloc[i, 1])


if __name__ == "__main__":
    main()
