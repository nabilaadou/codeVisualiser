from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import sys
sys.path.append('./app')
from pyTreeGenerator import pyGenerateTree

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"]   # Allow all headers like Content-Type
)

@app.post("/pySourceFiles")
async def root(request : Request):
	projectFiles = await request.json()
	response = pyGenerateTree(projectFiles)
	return response
