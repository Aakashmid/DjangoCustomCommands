from django.db import connection
from django.http import HttpRequest, HttpResponse
from CacheApp.models import Product
from django.core.cache import cache
import re

class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request: HttpRequest):        
        response = self.get_response(request)

        sample_model_table = Product._meta.db_table
    


        change_data_ids=[]
        
        for query in connection.queries :
            if sample_model_table in query['sql']:
                sql=query['sql'].lower()
                # print(query)

                # if 'insert into' in sql:
                #    # Find the position of RETURNING clause
                #     returning_index = sql.find('returning') + len('returning')
                    
                #     # Extract the substring after RETURNING clause
                #     id_value = sql[returning_index:].strip()
                    
                #     # Remove surrounding quotes and backticks (if any)
                #     id_value = id_value.strip('\'"')
                    
                #     print(f"Inserted ID value: {id_value}")

                if 'update' in sql:
                    # Extract ID from UPDATE query
                    id_match = re.search(r'where\s+.*?"CacheApp_product"\."id"\s*=\s*(\d+)', sql, re.IGNORECASE)
                    if id_match:
                        change_data_ids.append(id_match.group(1))
                    print(id_match.group(1))

                elif 'delete from' in sql:
                    # Extract ID from DELETE query
                    id_match = re.search(r'where\s+.*?"CacheApp_product"\."id"\s*in\s*\((\d+)\)', sql, re.IGNORECASE)
                    if id_match:
                        change_data_ids.append(id_match.group(1))
                    print(id_match.group(1))
            
        return response 

  


# import threading
# from django.db import connection
# from django.core.cache import cache
# from CacheApp.models import Product

# class CustomMiddleware:
#     thread_local = threading.local()

#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         # Capture initial state of the database
#         self.capture_initial_state()
        
#         response = self.get_response(request)
        
#         # Update cache if needed
#         self.update_cache_if_needed()
        
#         return response

#     def capture_initial_state(self):
#         # Capture the initial state of the relevant table rows
#         self.thread_local.initial_state = self.get_table_state()

#     def get_table_state(self):
#         # Implement logic to capture the current state of the table
#         # For example, select the relevant rows and their values
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT id, name, description, price FROM CacheApp_product")
#             return dict((row[0], row[1:]) for row in cursor.fetchall())

#     def update_cache_if_needed(self):
#         initial_state = self.thread_local.initial_state
#         current_state = self.get_table_state()

#         # print(f"Initial state :{initial_state}")
#         # print(f"current state {current_state}")
#         for id, values in current_state.items():
#             if id not in initial_state :
#                 self.update_cache_entry(id)
                
#             elif  initial_state[id] != values:
#                 self.update_cache_entry(id)
            
#         for id in initial_state.keys():
#             if id not in current_state:
#                 self.update_cache_entry(id)



    # def update_cache_entry(self, id):
    #     # Fetch the updated instance and update the cache
    #     instance = YourModel.objects.get(pk=id)
    #     cache.set(f'yourmodel_{id}', instance)

