#              - Ai Surfer 
#     /\__/\   - main.py 
#    ( o.o  )  - v0.0.1
#      >^<     - by @rUv

# Import the necessary modules and libraries
import os               # Provides access to operating system-dependent functionality
import openai           # OpenAI's GPT-3 language model library
import requests         # Library for making HTTP requests
from bs4 import BeautifulSoup  # Library for web scraping and parsing HTML/XML documents
from fastapi import FastAPI, Request  # FastAPI framework and Request object
from fastapi.responses import HTMLResponse  # HTML response class for FastAPI
from fastapi.templating import Jinja2Templates  # Templating engine for rendering HTML
from dataclasses import dataclass  # Utility for creating data classes
import spacy            # Library for natural language processing (NLP)
import asyncio          # Library for asynchronous programming
import httpx            # Library for making asynchronous HTTP requests
from fastapi.responses import FileResponse  # File response class for FastAPI
import mimetypes        # Library for determining the MIME type of a file

# Define an asynchronous function to fetch the HTML content of a URL
async def fetch_html(url: str) -> str:
    response = requests.get(url)  # Make an HTTP GET request to the URL
    return response.text          # Return the text content of the response

# Create a FastAPI application instance
app = FastAPI()

# Create a Jinja2Templates instance for rendering HTML templates
templates = Jinja2Templates(directory="templates")

# Set the OpenAI API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load the spaCy language model for English
nlp = spacy.load("en_core_web_sm")

# Define a data class to represent the URL data
@dataclass
class URLData:
    url: str  # URL string

# Define a function to extract Open Graph description data from a URL
def extract_opengraph_data(url):
    response = requests.get(url)  # Make an HTTP GET request to the URL
    soup = BeautifulSoup(response.content, "html.parser")  # Parse the HTML content of the response
    og_description = soup.find("meta", property="og:description")  # Find the Open Graph description meta tag
    # Return the content of the Open Graph description tag, if it exists, otherwise return None
    return og_description.get("content") if og_description else None

# Define a function to extract text content from an HTML string
def extract_text(url_content):
    soup = BeautifulSoup(url_content, "html.parser")  # Parse the HTML content
    text_parts = []  # Initialize an empty list to store text parts
    # Iterate over all <p> and <div> elements in the HTML and extract their text content
    for p in soup.find_all(["p", "div"]):
        text_parts.append(p.text)
    # Join the text parts with newline characters and return the result
    return "\n".join(text_parts)

# Define a function to extract keywords from a text string
def extract_keywords(text, num_keywords=5):
    doc = nlp(text)  # Process the text using the spaCy language model
    keywords = []  # Initialize an empty list to store keywords
    # Iterate over named entities in the text and extract keywords based on entity labels
    for ent in doc.ents:
        if ent.label_ in ["ORG", "PERSON", "GPE", "NORP"]:
            keywords.append(ent.text)
    # Iterate over tokens in the text and extract keywords based on part-of-speech tags
    for token in doc:
        if token.is_stop or token.is_punct:
            continue  # Skip stop words and punctuation
        if token.pos_ in ["NOUN", "ADJ", "VERB"] and len(keywords) < num_keywords:
            keywords.append(token.text)
    return keywords

# Define an asynchronous function to generate a summary of a text chunk using GPT-3
async def generate_summary_chunk(chunk):
    # Define the conversation messages for the GPT-3 model
    messages = [
        {"role": "system", "content": "You are an AI language model tasked with summarizing articles in bullet points."},
        {"role": "user", "content": f"Here's an article chunk to summarize:\n\n{chunk}\n\n"},
        {"role": "user", "content": "Provide the most interesting and important elements in an easy to understand way."}
    ]
    
    # Use an asynchronous HTTP client to make a POST request to the OpenAI API
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.openai.com/v1/chat/completions",  # API endpoint
            json={
                "model": "gpt-3.5-turbo-0301",  # Model name
                "messages": messages,  # Conversation messages
                "max_tokens": 100,  # Maximum number of tokens in the response
                "temperature": 0.9,  # Sampling temperature
                "n": 1,  # Number of completions to generate
                "stream": False,  # Streaming mode
                "stop": None,  # Stop sequence
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {openai.api_key}",  # API key for authorization
        },
    )

    response_data = response.json()
    summary = response_data['choices'][0]['message']['content'].strip()
    return summary  # Return the summary text

# Define an asynchronous function to generate a summary of an entire article
async def generate_summary(url):
    url_content = await fetch_html(url)  # Fetch the HTML content of the URL
    article = extract_text(url_content)  # Extract the text content from the HTML
    keywords = extract_keywords(article)  # Extract keywords from the article text
    
    chunk_size = 2800  # Define the maximum size of each article chunk
    # Split the article into chunks based on the defined chunk size
    article_chunks = [article[i:i + chunk_size] for i in range(0, len(article), chunk_size)]

    # Use concurrency to process chunks simultaneously and generate summaries for each chunk
    summaries = await asyncio.gather(*(generate_summary_chunk(chunk) for chunk in article_chunks))
    
    final_summary = "\n".join(summaries)  # Join the summaries to form the final summary
    return final_summary  # Return the final summary

# Define a route for the root URL ("/") that renders the index.html template
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Define a route for the "/api/summarize" endpoint that summarizes a given URL
@app.post("/api/summarize")
async def summarize_url(url_data: URLData):
  # Access the DOMAIN_NAME secret from the Replit environment
    domain_name = os.getenv("DOMAIN_NAME")
    og_description = extract_opengraph_data(url_data.url)  # Extract Open Graph description
    url_content = await fetch_html(url_data.url)  # Fetch the HTML content of the URL
    article = extract_text(url_content)  # Extract the text content from the HTML
    # Generate the summary using the Open Graph description or the generate_summary function
    summary = og_description if og_description else await generate_summary(url_data.url)
    keywords = extract_keywords(article)  # Extract keywords from the article text
    return {"summary": summary}  # Return the summary as a JSON response

# Define a route for the "/summary" endpoint that displays the summary
@app.get("/summary", response_class=HTMLResponse)
async def display_summary(request: Request):
    summary = request.query_params.get("summary", "No summary provided.")
    return templates.TemplateResponse("summary.html", {"request": request, "summary": summary})

# Define a route for serving files from the ".well-known" path
@app.get('/.well-known/{filename}')
async def download(filename: str):
    file_path = 'plugins/' + filename  # Construct the file path based on the filename
    media_type, _ = mimetypes.guess_type(file_path)  # Determine the MIME type of the file
    return FileResponse(file_path, media_type=media_type or 'text/plain')  # Serve the file

# Run the FastAPI application using the Uvicorn ASGI server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
