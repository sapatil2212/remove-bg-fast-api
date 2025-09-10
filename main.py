"""
Local development server for the Background Removal API
Run with: uvicorn main:app --reload --host 0.0.0.0 --port 8000
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import Response
from rembg import remove

app = FastAPI(
    title="Background Removal API",
    description="Remove background from images using AI",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {
        "message": "Background Removal API is running",
        "status": "healthy",
        "endpoints": {
            "remove_bg": "/removebg",
            "health": "/health",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "background-removal-api"}

@app.post("/removebg")
async def remove_bg(image: UploadFile = File(...)):
    """
    Remove background from uploaded image
    
    Args:
        image: Image file (PNG or JPEG)
    
    Returns:
        PNG image with background removed
    """
    # Validate file type
    if image.content_type not in ("image/png", "image/jpeg", "image/jpg"):
        raise HTTPException(
            status_code=400, 
            detail="Only PNG or JPEG images are allowed"
        )
    
    # Validate file size (max 10MB)
    if image.size and image.size > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="File size too large. Maximum size is 10MB"
        )
    
    try:
        # Read image data
        data = await image.read()
        
        # Process image to remove background
        output = remove(data)
        
        return Response(
            content=output, 
            media_type="image/png",
            headers={
                "Content-Disposition": f"attachment; filename=removed_bg_{image.filename or 'image'}.png"
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing image: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
