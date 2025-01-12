import os
import logging

from run.data_crossing import DataCrossing
from run.trace_malloc import MemoryUse
from utils.run_helper import build_df_cross_data, save_data_to_db

# Configuração de logging
logging.basicConfig(level=logging.INFO)


def main():
    # Monitorar uso de memória
    obj_memory_usage = MemoryUse()
    obj_memory_usage.add_checkpoint(name="Codigo iniciado!")

    # Caminho do arquivo Excel
    path_xlsx = os.path.join(os.getcwd(), "projecoes_2024_tab1_idade_simples.xlsx")

    # Construir os DataFrames
    obj_data = DataCrossing(path_xlsx=path_xlsx)
    build_df_cross_data(
        obj_memory_usage=obj_memory_usage, obj_data=obj_data, logging=logging
    )

    save_data_to_db(
        obj_memory_usage=obj_memory_usage, obj_data=obj_data, logging=logging
    )


if __name__ == "__main__":
    main()
