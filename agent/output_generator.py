import json


class OutputGenerator:

    @staticmethod
    def generate_status(
        incident_id,
        changes_applied,
        pr_url,
        status="SUCCESS"
    ):

        return {
            "incident_id": incident_id,
            "status": status,
            "changes_applied": changes_applied,
            "pull_request": pr_url
        }

    @staticmethod
    def save_output(
        path,
        output
    ):

        with open(path, "w") as file:
            json.dump(
                output,
                file,
                indent=4
            )