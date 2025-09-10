from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import Response
from rembg import remove

app = FastAPI(title="Rembg Service")

@app.post("/removebg")
async def remove_bg(image: UploadFile = File(...)):
    if image.content_type not in ("image/png", "image/jpeg"):
        raise HTTPException(status_code=400, detail="Only PNG or JPEG allowed")
    data = await image.read()
    try:
        output = remove(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"rembg error: {e}")
    return Response(content=output, media_type="image/png")


