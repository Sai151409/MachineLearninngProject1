from housing.pipeline.pipeline import Pipeline
from housing.logger import logging
from housing.config.configuration import Configuration
from housing.component.data_ingestion import DataIngestion
from housing.component.data_validation import DataValidation
from housing.config.configuration import Configuration

def main():
    try:
        data_ingestion_artifact = DataIngestion(data_ingestion_config=Configuration().get_data_ingestion_config())
        data_validation = DataValidation(data_validation_config=Configuration().get_data_validation_config(),
                                         data_ingestion_artifact=data_ingestion_artifact.intitate_data_ingestion())
        print(data_validation.validate_dataset_schema())
    except Exception as e:
        logging.error(f"{e}")
        print(e)
    
    
if __name__ == "__main__":
    main()
    
    