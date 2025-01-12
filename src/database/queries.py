from sqlalchemy import text

query_sexo_local = text(
    """
CREATE TABLE IF NOT EXISTS sexo_local (
    "ID" SERIAL PRIMARY KEY,
    "SEXO" VARCHAR(10) NOT NULL,
    "LOCAL" VARCHAR(100) NOT NULL,
    "TOTAL_ANOS" BIGINT NOT NULL
);
"""
)

query_idade_local = text(
    """
CREATE TABLE IF NOT EXISTS idade_local (
    "ID" SERIAL PRIMARY KEY,
    "IDADE" INTEGER NOT NULL,
    "LOCAL" VARCHAR(100) NOT NULL,
    "TOTAL_ANOS" BIGINT NOT NULL
);
"""
)

query_sexo_idade = text(
    """
CREATE TABLE IF NOT EXISTS sexo_idade (
    "ID" SERIAL PRIMARY KEY,
    "SEXO" VARCHAR(10) NOT NULL,
    "IDADE" INTEGER NOT NULL,
    "TOTAL_ANOS" BIGINT NOT NULL
);
"""
)
