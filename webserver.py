from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import markdown2

app = FastAPI()

# Mount the static folder to serve static files
app.mount("/", StaticFiles(directory="static"), name="static")


@app.get("/{filename:path}")
async def read_file(filename: str):

    # Path to the file
    file_path = Path("") / filename

    # Check if the file exists
    if file_path.is_file():
        # If the file is a Markdown file, convert it to HTML
        if file_path.suffix == ".md":
            with file_path.open("r", encoding="utf-8") as markdown_file:
                markdown_content = markdown_file.read()
                html_content = markdown2.markdown(markdown_content)
                return HTMLResponse(content=html_content)
        # If the file is an image file, return it as an image response
        elif file_path.suffix in [".jpg", ".jpeg", ".png", ".gif"]:
            return FileResponse(str(file_path))
        # For other file types, return them directly
        else:
            with file_path.open("r", encoding="utf-8") as file:
                return HTMLResponse(content=file.read())
    else:
        raise HTTPException(status_code=404, detail="File not found")


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=1235)
