from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os

router = APIRouter(prefix="/personagem")

class Personagem(BaseModel):
    nome: str
    vila: str
    descricao: str
    nome_arquivo_imagem: str

UPLOAD_DIRECTORY = os.path.join(os.getcwd(), "character", "model", "imagens")

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

personagens = []

@router.get("/personagens")
async def obter_personagens():
    return personagens


@router.post("/personagem/criar")
async def criar_personagem_com_imagem(
    imagem: UploadFile = File(...),
    nome: str = "nome",
    vila: str = "vila",
    descricao: str = "descrição"
):
    caminho_imagem = os.path.join(UPLOAD_DIRECTORY, imagem.filename)
    personagem = Personagem(nome=nome, vila=vila, descricao=descricao, nome_arquivo_imagem=imagem.filename)
    with open(caminho_imagem, "wb") as buffer:
        buffer.write(imagem.file.read())
        personagens.append(personagem)
    return {"mensagem": "Imagem carregada com sucesso"}


@router.get("/personagens/{nome_personagem}")
async def obter_imagem_personagem(nome_personagem: str):
    for personagem in personagens:
        if personagem.nome == nome_personagem:
            caminho_imagem = os.path.join(UPLOAD_DIRECTORY, personagem.nome_arquivo_imagem)
            if os.path.exists(caminho_imagem):
                return JSONResponse(content={"personagem": personagem.dict(), "caminho_imagem": caminho_imagem})
            else:
                return {"erro": "Imagem não encontrada para este personagem"}
    return {"erro": "Personagem não encontrado"}


@router.put("/personagens/{nome_personagem}")
async def atualizar_personagem(nome_personagem: str, personagem_atualizado: Personagem):
    for personagem in personagens:
        if personagem.nome == nome_personagem:
            # Verifica se os campos de atualização não estão vazios
            if personagem_atualizado.vila:
                personagem.vila = personagem_atualizado.vila
            if personagem_atualizado.descricao:
                personagem.descricao = personagem_atualizado.descricao

            # Verifica se o nome do personagem não está sendo alterado
            if personagem.nome != personagem_atualizado.nome:
                raise HTTPException(status_code=400, detail="O nome do personagem não pode ser alterado")

            return {"mensagem": f"Personagem {nome_personagem} atualizado com sucesso", "personagem": personagem}
    raise HTTPException(status_code=404, detail=f"Personagem {nome_personagem} não encontrado")


@router.delete("/personagens/{nome_personagem}")
async def deletar_personagem(nome_personagem: str):
    for personagem in personagens:
        if personagem.nome == nome_personagem:
            personagens.remove(personagem)
            caminho_imagem = os.path.join(UPLOAD_DIRECTORY, personagem.nome_arquivo_imagem)
            if os.path.exists(caminho_imagem):
                os.remove(caminho_imagem)
            return {"mensagem": f"Personagem {nome_personagem} excluído com sucesso"}
    raise HTTPException(status_code=404, detail=f"Personagem {nome_personagem} não encontrado")
