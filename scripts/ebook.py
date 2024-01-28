import os
import shutil
import pandas as pd


class Ebooks():
    def __init__(self, source_folder: os.path, transfer_folder: os.path):
        self.check_folder_existence(source_folder, "Source")
        self.check_folder_existence(transfer_folder, "Transfer")
        self.failed_books = []

    def check_folder_existence(self, folder_path: os.path, folder_name: str):
        if not os.path.exists(folder_path):
            raise Exception(f"{folder_name} folder not found: {folder_path}")
        setattr(self, f"{folder_name.lower()}_folder", folder_path)

    def check_book(self, author: str, title: str, display: bool = False):
        """Checks if the specified book exists in the source folder."""

        if ":" in title:
            title = title.replace(":", "_")

        if title.startswith("The "):
            title = title[4:] + ", The"

        if title.startswith("A "):
            title = title[2:] + ", A"

        title_folder = os.path.join(self.source_folder, author, title)
        result = os.path.exists(title_folder)

        if result:
            mobi_file = self.find_file_in_folder(title_folder, '.mobi')
            jpg_file = self.find_file_in_folder(title_folder, '.jpg')
            self.transfer_book(title_folder,mobi_file)
            self.transfer_book(title_folder,jpg_file)

        if display:
            if result:
                print(f"Found {title_folder}")
            else:
                print(f"Could not find {title_folder}")

        return result

    def transfer_book(self, source_folder: str, item: str):
        """Transfer the book files to the transfer folder."""

        try:

            file_name = os.path.basename(item)

            # Construct the full destination path
            full_source = os.path.join(source_folder, item)
            destination_path = os.path.join(self.transfer_folder, file_name)
            print(f"Copying {full_source} to {destination_path}")

            # Copy the file
            shutil.copy2(full_source, destination_path)

        except Exception as e:
            print(f"Error occurred: {e}")

    def batch_check_book(self, data: object):
        """Checks if the specified book exists in the source folder."""

        books = data.get_selected_books()
        for i in range(len(books)):
            if not self.check_book(books.iloc[i, 0], books.iloc[i, 1]):
                self.failed_books.append(f"{books.iloc[i, 0]} - {books.iloc[i, 1]}")

        print(f"{len(self.failed_books)} books could not be found")
        for i, book in enumerate(self.failed_books, 1):
            print(i, book)

    def find_file_in_folder(self, folder_path: os.path, extension: str):
        """Find a file with a given extension in the specified folder."""
        if os.path.exists(folder_path):
            for file in os.listdir(folder_path):
                if file.endswith(extension):
                    return os.path.join(folder_path, file)
        return 'n/a'

    def properties(self):
        """Prints the properties of the Ebooks object."""
        print("Ebooks object properties:")
        for i in self.__dict__:
            print(f"{i}: {self.__dict__[i]}")


class Inventory():
    """Object to store details of the csv that lists the books to be processed."""

    def __init__(self, source_path: os.path, file_name: str, cols: list, filter_by: str):

        self.source_path = source_path
        self.file_name = file_name
        self.cols = cols

        self.filter_col = filter_by.split('=')[0]
        self.filter_val = filter_by.split('=')[1]
        self.source_file = os.path.join(self.source_path, self.file_name)

        if not os.path.exists(self.source_file):
            raise Exception(f"File not found: {self.source_file}")

    def get_selected_books(self):
        """Returns a list of books that match the specified filter."""
        df = pd.read_csv(self.source_file, encoding='utf-8')
        df = df[df[self.filter_col] == self.filter_val]
        return df

    def properties(self):
        """Prints the properties of the Inventory object."""
        print("Inventory object properties:")
        for i in self.__dict__:
            print(f"{i}: {self.__dict__[i]}")


def main():
    data = Inventory(r"D:\OneDrive\Books", "five star books.csv", ['Title', 'Authors', 'Genres', 'Source', 'Ben'],
                     'Ben=Y')  # noqa: E501
    # data.properties()

    ebooks = Ebooks(r"\\MYCLOUDEX2ULTRA\Public\Books\5Start list\MOBI", r"D:\OneDrive\Books\pending transfer\ben")
    # ebooks.properties()
    ebooks.batch_check_book(data)


if __name__ == "__main__":
    main()
