from dotenv import load_dotenv
from src.utils.config import JobConfig
from src.agents.auto_cowriter_agent import AutoCowriterAgent


load_dotenv()


def run_job(config: JobConfig):
    cowriter_agent = AutoCowriterAgent(
        topic=config.topic,
        model_name=config.model_name,
        model_temperature=config.model_temperature,
        save_to_disk=config.save_to_disk,
    )
    cowriter_agent.run()
    cowriter_agent.write_to_airtable()


if __name__ == "__main__":
    config = JobConfig(
        topic="python decorators",
        model_name="gpt3.5",
        model_temperature=0.8,
        save_to_disk=False,
    )
    run_job(config)
