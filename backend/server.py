from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from diagramBuilder import diagram

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"]   # Allow all headers like Content-Type
)

@app.post("/diagram")
async def root(request : Request):
	projectFiles = await request.json()
	diagram(projectFiles)
	return {'recieved data': projectFiles}
