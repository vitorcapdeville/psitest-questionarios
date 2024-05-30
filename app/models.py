from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class PerguntaAlternativaLink(SQLModel, table=True):
    pergunta_id: Optional[int] = Field(default=None, foreign_key="pergunta.id", primary_key=True)
    alternativa_id: Optional[int] = Field(default=None, foreign_key="alternativa.id", primary_key=True)


class QuestionarioBase(SQLModel):
    nome: str = Field(index=True)
    descricao: Optional[str] = Field(default=None)


class Questionario(QuestionarioBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    perguntas: List["Pergunta"] = Relationship(back_populates="questionario")


class QuestionarioRead(QuestionarioBase):
    id: int


class PergntaBase(SQLModel):
    descricao: str = Field(index=True)

    questionario_id: Optional[int] = Field(default=None, foreign_key="questionario.id")


class Pergunta(PergntaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    questionario: Optional[Questionario] = Relationship(back_populates="perguntas")
    alternativas: List["Alternativa"] = Relationship(back_populates="perguntas", link_model=PerguntaAlternativaLink)


class AlternativaBase(SQLModel):
    descricao: str = Field(index=True)


class Alternativa(AlternativaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    descricao: str = Field(index=True)

    perguntas: List[Pergunta] = Relationship(back_populates="alternativas", link_model=PerguntaAlternativaLink)


class AlternativaRead(AlternativaBase):
    id: int


class PerguntaRead(PergntaBase):
    id: int
    alternativas: List[AlternativaRead]


class QuestionarioReadComPerguntas(QuestionarioRead):
    perguntas: List[PerguntaRead]
