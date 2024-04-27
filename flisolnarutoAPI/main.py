from fastapi import FastAPI
import uvicorn

from character.model.character_router import router as character_router  

app = FastAPI()

@app.get("/flisol")
def main() -> str:
    return "Oi galera do Flisol"

app.include_router(character_router)

if __name__ == "__main__":
    
    uvicorn.run(app, host="127.0.0.1", port=8000)
