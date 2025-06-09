import strawberry
from typing import List
from models import CategoriaContato, TipoTelefone, Telefone, Contato
from routes import contatos_db  

# Tipos GraphQL (usamos @strawberry.type)
@strawberry.type
class TelefoneType:
    numero: str
    tipo: str

@strawberry.type
class ContatoType:
    nome: str
    categoria: str
    telefones: List[TelefoneType]

# Resolver que transforma Contato (Pydantic) em ContatoType (Strawberry)
def to_graphql_contato(contato) -> ContatoType:
    telefones = [TelefoneType(numero=t.numero, tipo=t.tipo.value) for t in contato.telefones]
    return ContatoType(
        nome=contato.nome,
        categoria=contato.categoria.value,
        telefones=telefones
    )

@strawberry.type
class Query:
    @strawberry.field
    def listar_contatos(self) -> List[ContatoType]:
        return [to_graphql_contato(c) for c in contatos_db.values()]

    @strawberry.field
    def buscar_contato(self, nome: str) -> ContatoType:
        if nome not in contatos_db:
            raise Exception("Contato não encontrado")
        return to_graphql_contato(contatos_db[nome])

@strawberry.input
class TelefoneInput:
    numero: str
    tipo: str

@strawberry.type
class Mutation:
    @strawberry.mutation
    def criar_contato(self, nome: str, categoria: str, telefones: List[TelefoneInput]) -> ContatoType:
        if nome in contatos_db:
            raise Exception("Contato já existe")

        # Validar categoria e tipo dos telefones
        try:
            cat_enum = CategoriaContato(categoria)
        except ValueError:
            raise Exception("Categoria inválida")

        telefones_model = []
        for t in telefones:
            try:
                tipo_enum = TipoTelefone(t.tipo)
            except ValueError:
                raise Exception(f"Tipo de telefone inválido: {t.tipo}")
            telefones_model.append(
                Telefone(numero=t.numero, tipo=tipo_enum)
            )

        # Criar objeto Contato Pydantic

        contato_obj = Contato(nome=nome, categoria=cat_enum, telefones=telefones_model)
        contatos_db[nome] = contato_obj

        return to_graphql_contato(contato_obj)


schema = strawberry.Schema(query=Query, mutation=Mutation)
