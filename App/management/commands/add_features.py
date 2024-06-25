from django.core.management.base import BaseCommand
import requests
import os

class Command(BaseCommand):
    help = 'Add fetures by  downloads files from a github repository and processes them'

    def handle(self, *args, **kwargs):
        # Fetch the config file from the private repository
        self.stdout.write("Fetching the config file...")
        config = self.fetch_config()

        if config:
            #  Process the config file and download the files
            self.stdout.write("Processing the config file...")
            self.process_config(config)

            #  Print instructions
            self.stdout.write("All files downloaded and placed. Follow these instructions:")
            self.print_instructions(config)
        else:
            self.stdout.write(self.style.ERROR("Failed to fetch the config file."))

    def fetch_config(self):
        try:
            # URL to the config file in the private repository
            config_url = 'https://raw.githubusercontent.com/Aakashmid/DjangoRedis/main/config.json'


        
            response = requests.get(config_url)

            if response.status_code == 200:
                return response.json()
            else:
                self.stdout.write(self.style.ERROR(f"Failed to download config file: {response.status_code}"))
                return None
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {e}"))
            return None

    def process_config(self, config):
        for file_info in config.get('files', []):
            file_url = file_info['url']
            destination = file_info['destination']

            # Ensure the destination directory exists
            os.makedirs(os.path.dirname(destination), exist_ok=True)

            # Download the file
            self.download_file(file_url, destination)

    def download_file(self, url, destination):
        try:
            response = requests.get(url)

            if response.status_code == 200:
                with open(destination, 'wb') as f:
                    f.write(response.content)
                self.stdout.write(self.style.SUCCESS(f"Downloaded {url} to {destination}"))
            else:
                self.stdout.write(self.style.ERROR(f"Failed to download {url}: {response.status_code}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {e}"))

    def print_instructions(self, config):
        instructions = config.get('instructions', 'No specific instructions provided.')
        print(f'Instructions :  {instructions} ')
        input("Please review the instructions above and press Enter to continue...")
