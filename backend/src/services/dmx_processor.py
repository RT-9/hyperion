from fastapi import WebSocket

class DMXProcessor:
    
    def __init__(self, websocket:WebSocket):
        self.ws = websocket
    
    async def json_data(self, data):
        print(data)
        await self.ws.send_text("AAAAAAA")
        
    
        
    