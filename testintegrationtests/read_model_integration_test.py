from businessclasses.model_catalog import ModelCatalog
from dataio.model_catalog_db_data_io import ModelCatalogDbDataIo
from dataio.model_data_io import ModelDataIo
from businessclasses.config import Config

config = Config()
cip_numbers = config.unique_cip_numbers
model_catalog_dataio = ModelCatalogDbDataIo(config)
model_dataio = ModelDataIo(config, model_catalog_dataio)
model_catalog = ModelCatalog(config)
models = model_catalog.create_models_from_model_catalog_db(model_catalog_dataio)
pass