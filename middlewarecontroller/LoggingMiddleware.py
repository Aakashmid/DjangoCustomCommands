# middleware.py

import pymongo
from django.conf import settings
import json
from concurrent.futures import ThreadPoolExecutor

class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.client = pymongo.MongoClient('mongodb://localhost:27017')
        self.db = self.client['demoDb']
        self.collection = self.db['responses']
        self.executor = ThreadPoolExecutor(max_workers=5)  # for async operation

    def log_request_response(self, log_data):
        self.collection.insert_one(log_data)

    def __call__(self, request):
        request_log_data = {
            'method': request.method,
            'path': request.path,
            'GET': request.GET.dict(),
            'POST': request.POST.dict(),
            # 'body': request.body.decode('utf-8') if request.body else None,
            'headers': dict(request.headers),
        }
        
        response = self.get_response(request)
        
        request_log_data.update({
            'status_code': response.status_code,
            'response_content': response.content.decode('utf-8') if response.content else None,
            'response_headers': dict(response.items()),
        })
        
        self.executor.submit(self.log_request_response, request_log_data)
        
        return response
