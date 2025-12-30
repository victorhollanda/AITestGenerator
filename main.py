from parsers.swagger_parser import SwaggerParser
from generators.robot_framework_gen import RobotFrameworkGen

def main():
    parser = SwaggerParser()
    project_name = "TestesAPI"
    project_api = parser.parse("swagger.json")
    generator = RobotFrameworkGen()
    
    generator.generate_tests(project_name, project_api)

if __name__ == "__main__":
    main()
