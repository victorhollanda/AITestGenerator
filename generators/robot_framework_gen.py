from pathlib import Path
from core.models import Endpoint, Parameter, Response

class RobotFrameworkGen:

    def generate_tests(self, project_name, project_api: dict[str, dict[str, list[Endpoint]]], output_path: str = "./output"):
        base_path = Path(output_path) / project_name
        base_path.mkdir(parents=True, exist_ok=True)
        self._create_project_structure(base_path)

        for api_name, suites in project_api.items():
            tests_path = base_path / "tests" / "api" / api_name
            tests_path.mkdir(parents=True, exist_ok=True)

            for suite, endpoints in suites.items():
                self._create_project_file(suite, endpoints, tests_path)





    def _create_project_structure(self, base_path: str):
        base = Path(base_path)

        folders = [
            base / "resources" / "libs" / "bodys",
            base / "resources" / "steps",
            base / "tests" / "api",
        ]

        for folder in folders:
            folder.mkdir(parents=True, exist_ok=True)

    
    def _create_project_file(
        self,
        suite_name: str,
        endpoints: list[Endpoint],
        tests_path: Path
    ):
        file_path = tests_path / f"{suite_name}.robot"

        with file_path.open("w", encoding="utf-8") as f:
            f.write("*** Settings ***\n")
            f.write("Library    RequestsLibrary\n\n")
            f.write("*** Test Cases ***\n")

            for endpoint in endpoints:
                test_name = f"{endpoint.method} {endpoint.path}"
                f.write(f"{test_name}\n")
                f.write(f"    Log    {endpoint.summary}\n\n")