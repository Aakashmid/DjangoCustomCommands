from django.core.management.base import BaseCommand
import requests
import os
from django.conf import settings
from pymongo import MongoClient,errors


class Command(BaseCommand):
    help = 'Add fetures by  downloads files from a github repository and processes them'

    def handle(self, *args, **kwargs):
        # Fetch the config file from the private repository
        self.stdout.write("Fetching the main config file...")
        main_config_url='https://raw.githubusercontent.com/Aakashmid/DjangoRedis/main/main_config.json'
        config = self.fetch_config(main_config_url)

        if config:
            #  Process the config file and download the files
            self.stdout.write("Processing the main config file...")
            self.process_main_config(config)

            #  Print instructions
            self.stdout.write("processed main config file")
            # self.print_instructions(config)
        else:
            self.stdout.write(self.style.ERROR("Failed to fetch the config file."))

    def fetch_config(self,config_url):
        try:
            # URL to the config file in the private repository
            response = requests.get(config_url)
            if response.status_code == 200:
                return response.json()
            else:
                self.stdout.write(self.style.ERROR(f"Failed to download  config file: {response.status_code}"))
                return None
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {e}"))
            return None

    def process_main_config(self,config):
        for feature_congfig_url in config.get('features',[]):
            feature_config=self.fetch_config(feature_congfig_url)

            if feature_config:
                self.stdout.write('processing feature configuration file ...')
                self.process_feature_config(feature_config)
            else:
                self.stdout.write(self.style.ERROR("Failed to fetch the config file."))


    def process_feature_config(self, config):
        for file_info in config.get('files', []):
            file_url = file_info['url']
            destination = file_info['destination']
            # Ensure the destination directory exists
            os.makedirs(os.path.dirname(destination), exist_ok=True)

            # Download the file
            self.download_file(file_url, destination)

            self.print_instructions(file_info)

            # if file_info.get('needs_mongo',False):
            #     self.get_mongo_details()
            
        self.stdout.write(self.style.SUCCESS('SETUP COMPLETED'))

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

    # for getting mongodb details
    # def get_mongo_details(self):
    #     verify_details=False
    #     while(not verify_details):
    #         mongodb_url=input("Enter  url of your MonggoDb : ")
    #         db_name=input('Enter name of your MongoDb databaes : ')
    #         collection_name=input("Enter name of collection object of your MongoDb :")
    #         try: 
    #             client=MongoClient(mongodb_url)
    #             client.server_info()  #call to check server is accessible
    #             databases=client.list_database_names()

    #             if db_name in databases: # check db exist or not 
    #                 collections =  client[db_name].list_collection_names()
    #                 if collection_name not in collections: # verify collection object 
    #                     self.stdout.write(self.style.ERROR(f"Collection '{collection_name}' not found in database '{db_name}'."))
    #                     verify_details=False
    #                 else:
    #                     verify_details=True
                        
    #             else:
    #                 self.stdout.write(self.style.ERROR(f"Database '{db_name}' not found on the server."))
    #                 verify_details=False

    #         except errors.ConnectionError:
    #             self.stdout.write(self.style.ERROR("Could not connect to MongoDB server."))
    #             verify_details=False
    #         except errors.ServerSelectionTimeoutError:
    #             self.stdout.write(self.style.ERROR("MongoDB server selection timed out."))
    #             verify_details=False
        
    #     settings_file = os.path.join(settings.BASE_DIR, 'settings.py')
    #     with open(settings_file, 'r') as f:
    #         lines = f.readlines()
        
    #     mongo_settings = (
    #             f"\n# MongoDB settings for LoggingMiddleware\n"
    #             f"MONGODB_URL = '{mongodb_url}'\n"
    #             f"MONGODB_NAME = '{db_name}'\n"
    #             f"MONGODB_COLLECTION_NAME = '{collection_name}'\n"
    #         )
    #     lines.append(mongo_settings)

    #     with open(settings_file, 'w') as f:
    #         f.writelines(lines)
        
    #     self.stdout.write(self.style.SUCCESS("MongoDb connection is successfull and MongoDb details are added in  settings.py"))

    def print_instructions(self,file_info):
        print(file_info['instructions'])
        input('Follow above instrucion and then press enter...')
        if file_info.get('middleware_class',None):
            middleware_added=False
            while(not middleware_added):
                if file_info['middleware_class'] not  in  settings.MIDDLEWARE:
                    self.stdout.write(self.style.ERROR("Before continue add given middleware in settings.MIDDLEWARE !!"))
                    input('press enter to continue...')
                    middleware_added=False
                else:
                    middleware_added=True
            



                
            
        



