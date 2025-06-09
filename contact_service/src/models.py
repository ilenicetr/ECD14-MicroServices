from pydantic import BaseModel
from typing import List
from enum import Enum

#class Telefone(BaseModel):
 #   numero: str
  #  tipo: str  # "móvel", "fixo", "comercial"

#class Contato(BaseModel):
 #   nome: str
  #  telefones: List[Telefone]
   # categoria: str  # "familiar", "pessoal", "comercial" 

# Enums para categoria do contato e tipo do telefone
class CategoriaContato(str, Enum):
    familiar = "familiar"
    pessoal = "pessoal"
    comercial = "comercial"

class TipoTelefone(str, Enum):
    movel = "movel"
    fixo = "fixo"
    comercial = "comercial"

# Modelo para o número de telefone
class Telefone(BaseModel):
    numero: str
    tipo: TipoTelefone

# Modelo principal do contato
class Contato(BaseModel):
    nome: str
    categoria: CategoriaContato
    telefones: List[Telefone]