from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from graphql_schema import schema
from routes import router

app = FastAPI(
    title="API de Contatos",
    description="Uma API simples de agenda de contatos com Swagger UI",
    version="1.0.0"
)

# Router GraphQL em /graphql
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

# Router REST
app.include_router(router)