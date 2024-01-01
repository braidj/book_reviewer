"""Locates and extracts media files from a given directory
Used to prepare .mobis for conversion to .epub"""
import os
import logging
import shutil

class MediaLocator:
    def __init__(self, base_path,transfer_path):
        self.path = base_path
        self.transfer_path = transfer_path
        logging.basicConfig(filename='media_locator.log', level=logging.INFO,
                            format='%(asctime)s:%(levelname)s:%(message)s')

    def folder_exists(self, path):
        """Check if a folder exists and log the result."""
        if os.path.exists(path):
            return True
        else:
            logging.info(f"{path} Directory does not exist")
            return False

    def find_file_in_folder(self, folder_path, extension):
        """Find a file with a given extension in the specified folder."""
        if self.folder_exists(folder_path):
            for file in os.listdir(folder_path):
                if file.endswith(extension):
                    return os.path.join(folder_path, file)
        return 'n/a'


    def get_media(self, authors, title):
        """Locates paths to .mobi and .jpg files for the requested author / title."""
        success= False
        try:
            authors_folder = os.path.join(self.path, authors)
            title_folder = os.path.join(authors_folder, title)
            media_files = {'.mobi': 'n/a', '.jpg': 'n/a'}

            if self.folder_exists(authors_folder) and self.folder_exists(title_folder):
                logging.info(f"Found {title_folder}")
                print(f"Found {title_folder}")
                media_files['.mobi'] = self.find_file_in_folder(title_folder, '.mobi')
                media_files['.jpg'] = self.find_file_in_folder(title_folder, '.jpg')

                for media in media_files:
                    if media_files[media] != 'n/a':
                        detail = os.path.basename(media_files[media])
                        logging.info(f"Found {detail} file")
                        print(f"\t{detail} file")
                    else:
                        logging.info(f"/tCould not find {media} file")
            else:
                print(f"Could not find {title_folder}")

            self.move_media(media_files)

        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return {'.mobi': 'n/a', '.jpg': 'n/a'}

    def copy_file_to_directory(self,item):
        """Copies the specified file to the transfer folder"""
        try:
            # Ensure the destination directory exists
            if not os.path.exists(self.transfer_path):
                os.makedirs(self.transfer_path)

            # Extract the file name from the source path
            file_name = os.path.basename(item)

            # Construct the full destination path
            destination_path = os.path.join(self.transfer_path, file_name)

            # Copy the file
            shutil.copy2(item, destination_path)
            logging.info(f"File copied to {destination_path}")
        except Exception as e:
            print(f"Error occurred: {e}")
    def move_media(self,media):
        """Moves the media to the transfer folder"""
        if media['.mobi'] != 'n/a':
            self.copy_file_to_directory(media['.mobi'])
        if media['.jpg'] != 'n/a':
            self.copy_file_to_directory(media['.jpg'])
