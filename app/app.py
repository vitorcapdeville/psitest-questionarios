from typing import List, Optional

import strawberry
from fastapi import FastAPI
from sqlalchemy import select
from strawberry.fastapi import GraphQLRouter

import app.models as models
from app.database import get_session


@strawberry.type
class Questionario:
    id: strawberry.ID
    nome: str
    descricao: str
    perguntas: List["Pergunta"]

    @classmethod
    def marshal(cls, model: models.Questionario) -> "Questionario":
        return cls(
            id=strawberry.ID(str(model.id)),
            nome=model.nome,
            descricao=model.descricao,
            perguntas=[Pergunta.marshal(pergunta) for pergunta in model.perguntas],
        )


@strawberry.type
class Pergunta:
    id: strawberry.ID
    descricao: str
    alternativas: List["Alternativa"]

    @classmethod
    def marshal(cls, model: models.Pergunta) -> "Pergunta":
        return cls(
            id=strawberry.ID(str(model.id)),
            descricao=model.descricao,
            alternativas=[Alternativa.marshal(alternativa) for alternativa in model.alternativas],
        )


@strawberry.type
class Alternativa:
    id: strawberry.ID
    descricao: str

    @classmethod
    def marshal(cls, model: models.Alternativa) -> "Alternativa":
        return cls(id=strawberry.ID(str(model.id)), descricao=model.descricao)


@strawberry.type
class Query:
    @strawberry.field
    async def questionarios(self, id: Optional[int] = None) -> List[Questionario]:
        async with get_session() as session:
            sql = select(models.Questionario).order_by(models.Questionario.nome)
            if id is not None:
                sql = sql.where(models.Questionario.id == id)
            db_produtos = (await session.execute(sql)).scalars().unique().all()
        return [Questionario.marshal(produto) for produto in db_produtos]


schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/questionarios")
