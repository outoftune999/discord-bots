import os
import aiohttp
import json

class HttpClient:

    async def send_api_request(self, uri):
        async with aiohttp.ClientSession() as session:
            async with session.get(uri) as response:
                if response.status != 200 :
                    print(f'Received non-200 status {response.status}')
                responseBody = await response.text()
                responseJson = json.loads(responseBody)
                return responseJson