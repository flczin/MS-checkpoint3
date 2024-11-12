from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator, Field
from humps import camelize

def to_camel(str):
    return camelize(str)


class Diploma(BaseModel):
    nome: str
    nacionalidade: str
    estado: str
    data_nascimento: str
    documento: str
    data_conclusao: str
    curso: str
    carga_horaria: str
    data_emissao: str = Field(default_factory=lambda: datetime.now().strftime("%d/%m/%Y"))
    nome_assinatura: str
    cargo: str

    @field_validator("data_emissao", "data_conclusao", "data_nascimento", mode="before")
    def validate_date_format(cls, value):
        try:
            dt = datetime.strptime(value, "%d/%m/%Y")
            return dt.strftime("%d/%m/%Y")
        except ValueError:
            raise ValueError("Date must be in format dd/mm/yyyy")

    model_config = ConfigDict(extra='allow', alias_generator=to_camel)