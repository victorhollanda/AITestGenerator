from services.generate_tests import GenerateTests

def main():
    generator = GenerateTests()
    generator.generate_robot_tests_from_swagger("swagger.json")

if __name__ == "__main__":
    main()
