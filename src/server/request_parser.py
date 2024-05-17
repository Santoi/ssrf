import json

class RequestParser:
    def parse(request):
        # Create Dictionary
        parameters = dict()

        # Divide string
        partes = request.split('/')
        host_port = partes[0].split(':')

        parameters["Host"] = host_port[0]
        parameters["Is localhost"] = True if parameters["Host"].lower() == "localhost" else False

        parameters["Port"] = int(host_port[1])
        parameters["Image name"] = partes[1]

        parameters_json = json.dumps(parameters, indent=len(parameters))


        return parameters, parameters_json

def testing():
    # Request
    request = "localhost:8080/ejemplo.jpg"
    
    # Get parameters
    parameters, parameters_json = parse(request)
    print("Parameters Json:")
    print(parameters_json)
    
    # Print parameters
    print("Parameters:")
    for key, value in parameters.items():
        print(f"{key}: {value}")

