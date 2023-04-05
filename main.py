from typing import Union
from fastapi import FastAPI , Request
import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("FAKE_VALUE")
app = FastAPI()

@app.post("/api")
async def MainApi(request: Request):
    data = await request.json()
    print(data)
    try:
        return data[0].message.text
    except:
        pass
    data = {
        "type": "text", 
        "text": "Select your favorite food category or send me your location!",
        "quickReply": { 
            "items": [
            {
                "type": "action", 
                "imageUrl": "https://example.com/sushi.png",
                "action": {
                "type": "message",
                "label": "Sushi",
                "text": "Sushi"
                }
            },
            {
                "type": "action",
                "imageUrl": "https://example.com/tempura.png",
                "action": {
                "type": "message",
                "label": "Tempura",
                "text": "Tempura"
                }
            },
            {
                "type": "action", 
                "action": {
                "type": "location",
                "label": "Send location"
                }
            }
            ]
        }
    }
    return data

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q,"sss":"wewewe"}