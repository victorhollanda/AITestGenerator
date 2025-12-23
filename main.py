from parsers.swagger_parser import SwaggerParser
from generators.robot_framework_gen import RobotFrameworkGen

def main():
    parser = SwaggerParser()
    project = parser.parse("swagger.json")

    generator = RobotFrameworkGen()
    generator.generate_tests(project, output_path="./output")

if __name__ == "__main__":
    main()
