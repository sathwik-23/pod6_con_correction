import os

from dotenv import load_dotenv

from agent.json_reader import JsonReader
from agent.json_writer import JsonWriter
from agent.config_updater import ConfigUpdater
from agent.validator import ConfigValidator
from agent.output_generator import OutputGenerator
from agent.github_manager import GithubManager


load_dotenv(".env")


class ConfigCorrectionAgent:

    def process(self, resolution_file):

        resolution = JsonReader.read(
            resolution_file
        )

        config = JsonReader.read(
            resolution["config_file_path"]
        )

        for action in resolution["actions"]:

            ConfigUpdater.update_value(
                config,
                action["parameter"],
                action["new_value"]
            )

        JsonWriter.write(
            resolution["config_file_path"],
            config
        )

        if not ConfigValidator.validate(
            config,
            resolution["actions"]
        ):
            raise Exception(
                "Configuration validation failed"
            )

        github_manager = GithubManager(
            os.getenv("GITHUB_TOKEN"),
            os.getenv("GITHUB_REPOSITORY")
        )

        branch_name = github_manager.create_branch(
            resolution["incident_id"]
        )

        github_manager.update_file_in_branch(
            branch_name,
            resolution["config_file_path"],
            config
        )

        pr_url = github_manager.create_pull_request(
            branch_name,
            f"Fix {resolution['incident_id']}",
            "Automated configuration remediation"
        )

        output = OutputGenerator.generate_status(
            resolution["incident_id"],
            len(resolution["actions"]),
            pr_url
        )

        OutputGenerator.save_output(
            f"output/{resolution['incident_id']}_status.json",
            output
        )

        print("SUCCESS")
        print(f"PR URL: {pr_url}")


if __name__ == "__main__":

    agent = ConfigCorrectionAgent()

    agent.process(
        "Incidents/Resolution/INC103.json"
    )