import os
import logging

from data_cross.data_crossing import DataCrossing
from memory_monitor.memory_monitor import MemoryMonitor

# Configuração de logging
logging.basicConfig(level=logging.INFO)


def main():
    # Monitorar uso de memória
    obj_memory_usage = MemoryMonitor()
    obj_memory_usage.add_checkpoint(name="Codigo iniciado!")

    # Caminho do arquivo Excel
    path_xlsx = os.path.join(os.getcwd(), "projecoes_2024_tab1_idade_simples.xlsx")

    # Construir os DataFrames
    obj_data = DataCrossing(
        xlsx_name=path_xlsx, logging=logging, memory_usage=obj_memory_usage
    )
    obj_data.run()

    obj_data.save_data_to_db()


if __name__ == "__main__":
    main()
