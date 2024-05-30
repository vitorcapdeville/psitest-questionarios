from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy_utils import database_exists
from sqlmodel import Session, select

from app.dependencies import get_session
from app.models import (
    Questionario,
    QuestionarioRead,
    QuestionarioReadComPerguntas,
)

from app.database import criar_db_e_tabelas, criar_questionarios, engine

if not database_exists(engine.url):
    criar_db_e_tabelas()
    criar_questionarios()


app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def pegar_questionarios(session: Annotated[Session, Depends(get_session)]) -> list[QuestionarioRead]:
    questionarios = session.exec(select(Questionario)).all()
    return questionarios


@app.get("/{questionario_id}")
def pegar_questionario_com_perguntas(
    session: Annotated[Session, Depends(get_session)], questionario_id: int
) -> QuestionarioReadComPerguntas:
    questionario = session.get(Questionario, questionario_id)
    if not questionario:
        raise HTTPException(status_code=404, detail="Questionário não encontrado")
    return questionario
