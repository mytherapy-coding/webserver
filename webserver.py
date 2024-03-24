from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import markdown2

app = FastAPI()

# Mount the static folder to serve static files
#app.mount("/", StaticFiles(directory="static"), name="static")


@app.get("/{filename:path}")
async def read_file(filename: str):
    print(filename)
    # Path to the file
    filepath = Path("static") / filename
    # Check if the file exists
    if filepath.is_file():
        return FileResponse(str(filepath))
    
    # If the file is a Markdown file, convert it to HTML
    filepath = Path("static") / f'{filename}.html'
    if filepath.is_file():
        return FileResponse(str(filepath))
    
    filepath = Path("static") / f'{filename}.md'
    if filepath.is_file():
        print('found md')
        with filepath.open("r", encoding="utf-8") as markdown_file:
            markdown_content = markdown_file.read()
            html_content = markdown2.markdown(markdown_content)
            return HTMLResponse(content=html_content)
        
    # If the file is an image file, return it as an image response    
    raise HTTPException(status_code=404, detail="File not found")


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=1235)
