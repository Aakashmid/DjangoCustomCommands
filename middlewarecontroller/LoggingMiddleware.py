# using mongodb and async to store required request respone 

import asyncio
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from motor.motor_asyncio import AsyncIOMotorClient


class CustomMiddleware(MiddlewareMixin):
    def _init_(self, get_response):
        self.get_response = get_response
        # Initialize MongoDB client here
        self.client = AsyncIOMotorClient('mongodb://localhost:27017')
        self.db = self.client['demoDb']
        self.collection = self.db['responses']

    async def _call_(self, request):
        # Perform your asynchronous operation here
        await self.store_request(request)
        
        response = await self.get_response(request)
        return response

    async def store_request(self, request):
        # Example of storing request data asynchronously
        # Adjust according to your needs
        data = {
            "method": request.method,
            "path": request.path,
            "body": await request.body_async(),
            "headers": dict(request.META),
        }
        result=await self.collection.insert_one(data)
       

       