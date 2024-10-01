from fastapi.responses import StreamingResponse
import os
from fastapi import FastAPI
import aiofiles
from pathlib import Path
from tqdm.asyncio import tqdm_asyncio
import asyncio
from hypercorn.config import Config
from hypercorn.asyncio import serve


app = FastAPI()


path = Path(r'') # Enter Path Here



fname = os.path.basename(path)

@app.get("/")
def read_root():
    return "Welcome to Simple File Server. Visit /item for the file or use wget"
CHUNK_SIZE = 1024 * 1024 * 200

@app.get("/item")
async def down():
    async def iterfile():
       async with aiofiles.open(path, 'rb') as f:
            file_size = os.path.getsize(path)
            with tqdm_asyncio(total=file_size, unit='B', unit_scale=True, desc=f'Sending {fname}') as pbar:
                while chunk := await f.read(CHUNK_SIZE):
                    yield chunk
                    pbar.update(len(chunk))  # Update tqdm with the chunk size

    file_size = os.path.getsize(path)

    return StreamingResponse(iterfile(), headers={"Content-Length": str(file_size), 'Content-Disposition': f'''attachment; filename="{fname}"'''})


config = Config()
config.bind = ["0.0.0.0:80"]
config.alpn_protocols = ['h2']  # Enable HTTP/2

asyncio.run(serve(app, config))
