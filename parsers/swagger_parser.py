import json
from core.models import Endpoint, Parameter, Response


class SwaggerParser:
    def parse(self, file_path: str) -> list[Endpoint]:
        spec = self._load_file(file_path)
        endpoints: list[Endpoint] = []

        paths = spec.get("paths", {})

        for path, methods in paths.items():
            for method, data in methods.items():
                print(method)
                endpoint = Endpoint(
                    path= path,
                    method= method.upper(),
                    summary= data.get("summary", ""),
                    parameters= self._parse_parameters(data),
                    request_body= self._parse_request_body(data),
                    responses= self._parse_responses(data),
                )
                endpoints.append(endpoint)

        return endpoints

    def _load_file(self, file_path: str) -> dict:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _parse_parameters(self, data: dict) -> list[Parameter]:
        parameters = []

        for param in data.get("parameters", []):
            parameters.append(
                Parameter(
                    name=param.get("name"),
                    location=param.get("in"),
                    required=param.get("required", False),
                    schema=param.get("schema", {}),
                )
            )

        return parameters

    def _parse_request_body(self, data: dict):
        request_body = data.get("requestBody")
        if not request_body:
            return None

        content = request_body.get("content", {})
        if "application/json" in content:
            return content["application/json"].get("schema")

        return None

    def _parse_responses(self, data: dict) -> list[Response]:
        responses = []

        for status_code, response_data in data.get("responses", {}).items():
            try:
                status = int(status_code)
            except ValueError:
                continue

            responses.append(
                Response(
                    status_code=status,
                    description=response_data.get("description", ""),
                    schema=self._extract_response_schema(response_data),
                )
            )

        return responses
    
    def _extract_response_schema(self, response_data: dict) -> dict:
        content = response_data.get("content", {})
        if "application/json" in content:
            return content["application/json"].get("schema", {})
        
        return {}


parse=SwaggerParser()

teste = parse.parse('H:/repos/AITestGenerator/swagger.json')
print(teste)