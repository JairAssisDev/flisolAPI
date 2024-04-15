from fastapi import FastAPI
from character.model.character_router import router as character_router  # Corrija a importação aqui

app = FastAPI()

@app.get("/flisol")
def main() -> str:
    return "oi galera"

app.include_router(character_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
