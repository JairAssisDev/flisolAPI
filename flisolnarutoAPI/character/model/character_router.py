from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel


router = APIRouter(prefix="/personagem")

class Personagem(BaseModel):
    nome: str
    vila: str
    descricao: str
   

personagens = []

@router.get("/personagens")
async def obter_personagens():
    return personagens


@router.post("/personagem/criar")
async def criar_personagem_com_imagem(
    nome: str = "nome",
    vila: str = "vila",
    descricao: str = "descrição"
):
    personagem = Personagem(nome=nome, vila=vila, descricao=descricao)
    personagens.append(personagem)
    return {"mensagem": "Imagem carregada com sucesso"}


@router.get("/personagens/{nome_personagem}")
async def obter_imagem_personagem(nome_personagem: str):
    for personagem in personagens:
        if personagem.nome == nome_personagem:
            return JSONResponse(content={"personagem": personagem.dict()})



@router.put("/personagens/{nome_personagem}")
async def atualizar_personagem(nome_personagem: str, personagem_atualizado: Personagem):
    for personagem in personagens:
        if personagem.nome == nome_personagem:
            if personagem_atualizado.vila:
                personagem.vila = personagem_atualizado.vila
            if personagem_atualizado.descricao:
                personagem.descricao = personagem_atualizado.descricao
            return {"mensagem": f"Personagem {nome_personagem} atualizado com sucesso", "personagem": personagem}
    raise HTTPException(status_code=404, detail=f"Personagem {nome_personagem} não encontrado")


@router.delete("/personagens/{nome_personagem}")
async def deletar_personagem(nome_personagem: str):
    for personagem in personagens:
        if personagem.nome == nome_personagem:
            personagens.remove(personagem)
            return {"mensagem": f"Personagem {nome_personagem} excluído com sucesso"}
    raise HTTPException(status_code=404, detail=f"Personagem {nome_personagem} não encontrado")
