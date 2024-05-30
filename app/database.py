from sqlmodel import Session, SQLModel, create_engine

from app.models import (
    Alternativa,
    Pergunta,
    PerguntaAlternativaLink,  # noqa: F401
    Questionario,
)

sqlite_file_name = "database.sqlite"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=False, connect_args=connect_args)


def criar_db_e_tabelas():
    SQLModel.metadata.create_all(engine)


def criar_questionarios():
    with Session(engine) as session:
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

        session.commit()
