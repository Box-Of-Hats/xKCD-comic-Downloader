"""A download client to download xkcd comics. 
By default, will download all xkcd comics up to the latest comic into the comics/ directory.
"""
import glob
import os
import re
import requests
import subprocess
import time

class ComicDownloader():
    """A client to download xkcd comics. 
    Takes a folderpath to save images to."""

    def __init__(self, folder, echo=True, output_stream=print):
        self.folder = folder
        self.echo = echo
        self.output_stream = output_stream
        self.status_codes = {
            404: 'Page Not Found',
        }
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)

    def write_to_disk(self, url, filepath):
        """Writes file to disk, using a given url and filename"""
        file_request = requests.get(url, stream=True, )
        with open(filepath, 'wb') as new_file:
            for chunk in file_request.iter_content(chunk_size=1024):
                if chunk:
                    new_file.write(chunk)
        return filepath

    def download_comic(self, comic_number, filename=False):
        """Download a single comic, based on its comic number"""
        url = 'http://xkcd.com/{}/info.0.json'.format(comic_number)
        comic_request = requests.get(url)

        if comic_request.status_code in self.status_codes:
            self.output_stream('Issue with page request for url: \'{}\''.format(url))
            self.output_stream('{}: {}'.format(comic_request.status_code,
                                               self.status_codes[comic_request.status_code]))
            return False

        else:
            try:
                comic_attr = comic_request.json()
            except ValueError:
                self.output_stream('Could not parse JSON: comic no {}'.format(comic_number))
            if not filename:
                filename = '{}\\{}.png'.format(self.folder, comic_attr['num'])
            self.output_stream('Downloading: {}'.format(filename))
            self.write_to_disk(comic_attr['img'], filename)
            return True

    def download_latest(self, filename=False):
        """Downloads the latest comic only"""
        url = 'http://xkcd.com/info.0.json'
        comic_request = requests.get(url)
        comic_attr = comic_request.json()
        if not filename:
            filename = '{}\\{}.png'.format(self.folder, comic_attr['num'])
        self.write_to_disk(comic_attr['img'], filename)

    def current_highest(self):
        """Finds the highest comic number in the folder"""
        all_files = glob.glob('{}\\**'.format(self.folder))
        filenames = [int(''.join(re.findall(r'\d', fn.split('\\')[-1]))) for fn in all_files]
        if len(filenames) > 0:
            return max(filenames)
        else:
            return 0

    def download_range(self, lower, upper, delay=0.05):
        """Download x comics in a given number range, inclusive"""
        errors = 0
        downloaded_comics_counter = 0
        for comic_count in range(lower, upper+1):
            if errors > 3:
                break
            if not self.download_comic(comic_count):
                errors += 1
            else:
                downloaded_comics_counter += 1
                errors = 0
            time.sleep(delay)
        return downloaded_comics_counter

def main():
    """
    Called if module is directly run.
    Downloads all comics up to the latest comic, from the current highest
    """
    folder_to_save_to = 'comics'
    download_client = ComicDownloader(folder_to_save_to)
    comic_counter = download_client.download_range(download_client.current_highest()+1, 100000, 0)
    print('_'*70)
    print('\n')
    if comic_counter > 0:
        print('Finished downloading comics.')
        print('{} comics downloaded.'.format(comic_counter))
        subprocess.call(['explorer', folder_to_save_to])
    else:
        print('Comic collection is already up-to-date.')
        print('No comics downloaded.')
        input()


if __name__ == '__main__':
    main()
