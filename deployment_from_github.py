from pipeline_flow import main_pipeline

if __name__ == "__main__":
    deployment = main_pipeline.deploy(
        name="weather-etl-deployment",
        work_pool_name="cloud-pool",
        parameters={
            "data_dir": "data/",
            "output_path": "extracted_data/state_panel.csv",
            "api_key": ""
        }
    )
    deployment.apply()




