from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.models import (
    Alternativa,
    Base,
    Pergunta,
    PerguntaAlternativaLink,  # noqa: F401
    Questionario,
)

sqlite_file_name = "database.sqlite"
sqlite_url = f"sqlite+aiosqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=False, connect_args=connect_args)


engine = create_async_engine(sqlite_url, connect_args={"check_same_thread": False}, echo=False)

# Instancia um criador de seção com o banco
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        async with session.begin():
            try:
                yield session
            finally:
                await session.close()


async def _async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()


async def criar_questionarios():
    async with get_session() as session:
        # with Session(engine) as session:
        questionario1 = Questionario(nome="Questionario de teste 1", descricao="primeiro questionario de teste")
        alternativa1 = Alternativa(descricao="primeira opcao")
        alternativa2 = Alternativa(descricao="segunda opcao")
        alternativa3 = Alternativa(descricao="terceira opcao")
        alternativas = [alternativa1, alternativa2, alternativa3]
        pergunta1 = Pergunta(
            descricao="Pergunta de teste numero 1?",
            questionario=questionario1,
            alternativas=alternativas,
        )
        pergunta2 = Pergunta(
            descricao="Pergunta de teste numero 2?",
            questionario=questionario1,
            alternativas=alternativas,
        )
        pergunta3 = Pergunta(
            descricao="Pergunta de teste numero 3?",
            questionario=questionario1,
            alternativas=alternativas,
        )

        questionario2 = Questionario(nome="Questionario de teste 2", descricao="segundo questionario de teste")
        pergunta4 = Pergunta(
            descricao="Pergunta de teste numero 4?",
            questionario=questionario2,
            alternativas=alternativas,
        )
        pergunta5 = Pergunta(
            descricao="Pergunta de teste numero 5?",
            questionario=questionario2,
            alternativas=alternativas,
        )

        session.add(pergunta1)
        session.add(pergunta2)
        session.add(pergunta3)
        session.add(pergunta4)
        session.add(pergunta5)

        await session.commit()
