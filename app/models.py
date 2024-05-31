from typing import List, Optional
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from sqlalchemy import Column
from sqlalchemy import Table
from sqlalchemy import ForeignKey


class Base(DeclarativeBase):
    pass


PerguntaAlternativaLink = Table(
    "perguntaalternativalink",
    Base.metadata,
    Column("pergunta_id", ForeignKey("pergunta.id"), primary_key=True),
    Column("alternativa_id", ForeignKey("alternativa.id"), primary_key=True),
)


class Questionario(Base):
    __tablename__ = "questionario"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(index=True)
    descricao: Mapped[Optional[str]] = mapped_column(default=None)
    perguntas: Mapped[List["Pergunta"]] = relationship(back_populates="questionario", lazy="joined")


class Pergunta(Base):
    __tablename__ = "pergunta"

    id: Mapped[int] = mapped_column(primary_key=True)
    descricao: Mapped[str] = mapped_column(index=True)

    questionario_id: Mapped[int] = mapped_column(ForeignKey("questionario.id"))
    questionario: Mapped[Optional[Questionario]] = relationship(back_populates="perguntas")
    alternativas: Mapped[List["Alternativa"]] = relationship(
        back_populates="perguntas", secondary=PerguntaAlternativaLink, lazy="joined"
    )


class Alternativa(Base):
    __tablename__ = "alternativa"

    id: Mapped[int] = mapped_column(primary_key=True)
    descricao: Mapped[str] = mapped_column(index=True)

    perguntas: Mapped[List[Pergunta]] = relationship(back_populates="alternativas", secondary=PerguntaAlternativaLink)
