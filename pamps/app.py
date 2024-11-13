from fastapi import FastAPI

app = FastAPI(
    title= "Pamps",
    version="0.1.0",
    descriptions="Pamps is a posting app",   
)
# ooii
@app.get('/')
async def index():
    return {"Hello": "World"}

# @app.get('/')
# async def molho():
#     return{"ai": "papai"}