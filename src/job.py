from argparse import ArgumentParser
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
    argument_parser = ArgumentParser()
    argument_parser.add_argument("--topic", type=str, default="python decorators")
    argument_parser.add_argument(
        "--model_name",
        type=str,
        default="gpt3.5",
        choices=["gpt3.5", "gpt4", "davinci"],
    )
    argument_parser.add_argument(
        "--model_temperature",
        type=float,
        default=0.8,
    )
    argument_parser.add_argument(
        "--save_to_disk",
        type=bool,
        default=False,
    )
    args = argument_parser.parse_args()
    config = JobConfig(**vars(args))
    run_job(config)
