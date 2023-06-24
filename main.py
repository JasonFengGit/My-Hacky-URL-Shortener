from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
import secrets
import pickle
import os

class Url(BaseModel):
    url: str

app = FastAPI()

def load_urls():
    if os.path.exists('urls.pkl'):
        with open('urls.pkl', 'rb') as f:
            d = pickle.load(f)
            d["703e64"] = "https://twitter.com/64bits_ai"
            d["167e3f"] = "https://twitter.com/64bits_ai"
            return d
    else:
        return {"703e64":"https://twitter.com/64bits_ai", "167e3f":"https://twitter.com/64bits_ai"}

def save_urls(urls):
    with open('urls.pkl', 'wb') as f:
        pickle.dump(urls, f)

@app.get("/{short_url}")
async def read_url(short_url: str):
    urls = load_urls()
    url = urls.get(short_url)
    if url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    response = Response(headers={"Location": url})
    response.status_code = 303
    return response

@app.post("/shorten/")
async def shorten_url(url: Url):
    short_url = secrets.token_hex(3)  # Generate a random 6-character hex string
    urls = load_urls()
    while short_url in urls:
        short_url = secrets.token_hex(3)  # Regenerate if the URL is already in use
    urls[short_url] = url.url
    save_urls(urls)
    return {"short_url": short_url}
