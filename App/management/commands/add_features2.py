from django.core.management.base import BaseCommand
import requests
import os,re
from django.conf import settings
from pymongo import MongoClient,errors


class Command(BaseCommand):
    help = 'Add fetures by  downloads files from a github repository and processes them'

        # get path of settings.py 
    for root, dirs, files in os.walk(settings.BASE_DIR):
        if 'settings.py' in files:
            settings_file_path = os.path.join(root, 'settings.py')
            break
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

            if file_info.get('needs_mongo',False):
                self.get_mongo_details()
            
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
    def get_mongo_details(self):
        verify_details=False
        while(not verify_details):
            mongodb_url=input("Enter  url of your MonggoDb : ")
            db_name=input('Enter name of your MongoDb databaes : ')
            collection_name=input("Enter name of collection object of your MongoDb :")
            try: 
                client=MongoClient(mongodb_url)
                client.server_info()  #call to check server is accessible
                databases=client.list_database_names()

                if db_name in databases: # check db exist or not 
                    collections =  client[db_name].list_collection_names()
                    if collection_name not in collections: # verify collection object 
                        self.stdout.write(self.style.ERROR(f"Collection '{collection_name}' not found in database '{db_name}'."))
                        verify_details=False
                    else:
                        verify_details=True
                        
                else:
                    self.stdout.write(self.style.ERROR(f"Database '{db_name}' not found on the server."))
                    verify_details=False

            except errors.OperationFailure:
                self.stdout.write(self.style.ERROR("Could not connect to MongoDB server."))
                verify_details=False
            except errors.ServerSelectionTimeoutError:
                self.stdout.write(self.style.ERROR("MongoDB server selection timed out."))
                verify_details=False
        
        with open(self.settings_file_path, 'r') as f:
            lines = f.readlines()
        
        mongo_settings = (
                f"\n# MongoDB settings for LoggingMiddleware\n"
                f"MONGODB_URL = '{mongodb_url}'\n"
                f"MONGODB_NAME = '{db_name}'\n"
                f"MONGODB_COLLECTION_NAME = '{collection_name}'\n"
            )
        lines.append(mongo_settings)

        with open(self.settings_file_path, 'w') as f:
            f.writelines(lines)
        
        self.stdout.write(self.style.SUCCESS("MongoDb connection is successfull and MongoDb details are added in  settings.py"))

    def print_instructions(self,file_info):
        # from importlib import reload,import_module
        print(file_info['instructions'])
        input('To use new feature Follow above instrucion and then press enter...')

        #  write logic for validating that middleware is added or not 
        # if file_info.get('middleware_class',None):
        #     middleware_added=False
        #     while(not middleware_added):
        #         try:
        #             middleware_to_check=file_info['middleware_class']
        #             print(middleware_to_check)
        #             with open(self.settings_file_path, 'r') as f:
        #                 settings_content = f.read()
                        
        #                 # Find the start of the MIDDLEWARE setting
        #                 pattern = r"(?<=MIDDLEWARE\s*=\s*\[)[^\]]*(?=\])"
        #                 matches=re.search(pattern,settings_content)
        #                 if matches:
        #                     # Extract the list of middleware classes
        #                     middleware_list_str = matches.group(0)
        #                     middleware_list = re.findall(r"'(.*?)'",middleware_list_str)
        #                     middleware_list = [class_name.strip() for class_name in middleware_list]
        #                     # Check if the middleware is in the list
        #                     print(middleware_list)
        #                     if middleware_to_check in middleware_list:
        #                         self.stdout.write(self.style.SUCCESS(f"'{middleware_to_check}' is already added in MIDDLEWARE."))
        #                         middleware_added=True

        #                     else:
        #                         self.stdout.write(self.style.WARNING(f"'{middleware_to_check}' is not added in MIDDLEWARE yet."))
        #                         self.stdout.write(self.style.ERROR('middleware is not added in settings.MIDDLEWARE ,  add middleware to continue !'))
        #                         input('Enter if you added middleware ...')
                      

                                

        #         except FileNotFoundError:
        #             self.stdout.write(self.style.ERROR("settings.py file not found."))
                
                



                
            
        



