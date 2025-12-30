from parsers.swagger_parser import SwaggerParser
from generators.robot_framework_gen import RobotFrameworkGen
from generators.playwright_gen import PlaywrightGen

class GenerateTests:

    def generate_robot_tests_from_swagger(self, swagger_path: str):
        parser = SwaggerParser()
        generator = RobotFrameworkGen()
        project_name = "RobotFrameworkTests"
        project_api = parser.parse(swagger_path)

        generator.generate_tests(project_name, project_api)

    def generate_playwright_tests_from_swagger(self, swagger_path: str):
        parser = SwaggerParser()
        generator = PlaywrightGen()
        project_name = "PlaywrightTests"
        project_api = parser.parse(swagger_path)

        generator.generate_tests(project_name, project_api)