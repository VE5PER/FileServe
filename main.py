from fastapi.responses import StreamingResponse
import os
from fastapi import FastAPI
import aiofiles
from pathlib import Path

import asyncio
from hypercorn.config import Config
from hypercorn.asyncio import serve
app = FastAPI()
path = Path('') # Enter Path Here



fname = os.path.basename(path)

@app.get("/")
def read_root():
    return "Welcome to Simple File Server. Visit /item for the file"
CHUNK_SIZE = 1024 * 1024 * 10

@app.get("/item")
async def down():
    async def iterfile():
       async with aiofiles.open(path, 'rb') as f:
            while chunk := await f.read(CHUNK_SIZE):
                yield chunk
    
    file_size = os.path.getsize(path)
    
    return StreamingResponse(iterfile(), headers={"Content-Length": str(file_size),'Content-Disposition': f'''attachment; filename="{fname}"'''})


config = Config()
config.bind = ["0.0.0.0:8080"]

asyncio.run(serve(app, config))
