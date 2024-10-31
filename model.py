from pydantic import BaseModel, ConfigDict

class Diploma(BaseModel):
    nome_aluno: str
    nacionalidade: str
    estado: str
    nascimento: str
    rg: str
    conclusao: str
    curso: str
    carga_horaria: str
    emissao: str
    nome_ass: str
    cargo_ass: str

    model_config = ConfigDict(extra='allow')