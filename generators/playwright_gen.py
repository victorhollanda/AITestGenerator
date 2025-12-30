from pathlib import Path
import re
from core.models import Endpoint
import subprocess
from pathlib import Path
import re

class PlaywrightGen:

    def generate_tests(self, project_name, project_api: dict[str, dict[str, list[Endpoint]]], output_path: str = "./output"):
        base_path = Path(output_path) / project_name
        base_path.mkdir(parents=True, exist_ok=True)
        self._create_project_structure(base_path)

        for api_name, suites in project_api.items():
            tests_path = base_path / "tests" / "api" / api_name
            tests_path.mkdir(parents=True, exist_ok=True)

            for suite, endpoints in suites.items():
                self._create_suite_file(suite, endpoints, tests_path)

    def _create_project_structure(self, path: str):
        project_path = Path(path)

        try:
            subprocess.run(
                ["node", "--version"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise EnvironmentError(
                "Node.js não está instalado ou não está no PATH."
            )

        project_path.mkdir(parents=True, exist_ok=True)

        commands = [
            ["npm.cmd", "init", "-y"],
            ["npm.cmd", "i", "-D", "@playwright/test"]
        ]

        for command in commands:
            subprocess.run(
                command,
                cwd=project_path,
                check=True
            )

        folders = [
            project_path / "tests" / "api",
            project_path / "src" / "config",
            project_path / "src" / "builders"
        ]

        for folder in folders:
            folder.mkdir(parents=True, exist_ok=True)


    def format_payload_build_name(self, method: str, path: str) -> str:
        parts = path.strip('/').split('/')

        filtered = []
        for part in parts:
            # remove chaves imediatamente
            part = part.strip('{}')

            # ignora api e versões
            if part.lower() == 'api':
                continue
            if re.match(r'v\d+', part.lower()):
                continue

            filtered.append(part)

        # capitaliza
        name = ''.join(p.capitalize() for p in filtered)

        return f"build{method.upper()}{name}"

            
    def _create_suite_file(
        self,
        suite_name: str,
        endpoints: list[Endpoint],
        tests_path: Path
    ):
        file_path = tests_path / f"{suite_name}.spec.ts"

        with file_path.open("w", encoding="utf-8") as f:
            f.write("import { test, expect } from '@playwright/test';\n\n")
            f.write(f"test.describe('{suite_name}', () => {{\n\n")

            for index, endpoint in enumerate(endpoints):
                if index < 10:
                    test_name = f"TC0{index+1} - {endpoint.method.upper()} {endpoint.path}"
                else:
                    test_name = f"TC{index+1} - {endpoint.method.upper()} {endpoint.path}"

                payload_build_name = self.format_payload_build_name(endpoint.method, endpoint.path)

                f.write(f"  test('{test_name}', async ({{ request }}) => {{\n")
                f.write(f"      const payload = {payload_build_name};\n\n")
                f.write(f"      const response = await request.{endpoint.method}('{endpoint.path}', {{\n")
                f.write(f"          data: payload,\n")
                f.write(f"      }});\n\n")
                f.write(f"      expect(response.status()).toBe(888);\n")
                f.write(f"  }});\n\n")
            f.write(f"}});\n")
