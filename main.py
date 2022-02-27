import numpy as np
from PIL import Image
from fastapi import FastAPI, File, UploadFile
from GUI import main
import uvicorn
from io import BytesIO

app = FastAPI()

@app.get("/test")
def test():
    return "Finally..."

def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image

@app.post("/post_image")
async def post_image(file: UploadFile = File(...)):
    image = read_file_as_image(await file.read())
    main(image)

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)









