import sys
import importlib
import json
from lib.json_creator import *
from lib.graph_definitions import *


def run_frontend(frontend, source_code, max_params):
    try:
        module_class_pair = frontend.split(".")
        if len(module_class_pair) != 2:
            raise ValueError
        frontend = importlib.import_module("modules.frontends."+module_class_pair[0])
        FrontendClass = getattr(frontend, module_class_pair[1])

        frontend_obj = FrontendClass()
        frontend_obj.parse_signature(source_code, max_params)

    except (ModuleNotFoundError, ValueError, AttributeError):
        print("Frontend not found or invalid, exiting...")
        sys.exit(1)


def run_frontend(frontend, source_code, max_params):
    try:
        module_class_pair = frontend.split(".")
        if len(module_class_pair) != 2:
            raise ValueError
        frontend = importlib.import_module("modules.frontends."+module_class_pair[0])
        FrontendClass = getattr(frontend, module_class_pair[1])

        frontend_obj = FrontendClass()
        frontend_obj.parse_signature(source_code, max_params)
        # TODO: actually create the json file bc the current json function is fucked

    except (ModuleNotFoundError, ValueError, AttributeError):
        print("Frontend not found or invalid, exiting...")
        sys.exit(1)


def run_packer(packer, filename):
    try:
        module_class_pair = packer.split(".")
        if len(module_class_pair) != 2:
            raise ValueError
        packer = importlib.import_module("modules.packers."+module_class_pair[0])
        PackerClass = getattr(packer, module_class_pair[1])

        with open(filename, 'r') as f:
            contents = json.loads(f.read())

        functions = convert_json_to_parameter(contents)
        packer_obj = PackerClass(functions)
        packer_obj.minimize()
        return packer_obj.functions, packer_obj.packed_params

    except (ModuleNotFoundError, ValueError, AttributeError):
        print("Packer not found or invalid, exiting...")
        sys.exit(1)


def run_reconstructor(reconstructor, functions, packed_objs, filename):
    try:
        module_class_pair = reconstructor.split(".")
        if len(module_class_pair) != 2:
            raise ValueError
        reconstructor = importlib.import_module("modules.reconstructors." + module_class_pair[0])
        ReconstructorClass = getattr(reconstructor, module_class_pair[1])
        reconstructor_obj = ReconstructorClass()
        reconstructor_obj.reconstruct(functions, packed_objs, filename)

    except (ModuleNotFoundError, ValueError, AttributeError):
        print("Reconstructor not found or invalid, exiting...")
        sys.exit(1)


def run_metrics(metric, filename, functions, packed_objs):
    try:
        module_class_pair = metric.split(".")
        if len(module_class_pair) != 2:
            raise ValueError
        metric = importlib.import_module("modules.metrics." + module_class_pair[0])
        MetricClass = getattr(metric, module_class_pair[1])
        metric_obj = MetricClass()
        metric_obj.calculate_metrics()

    except (ModuleNotFoundError, ValueError, AttributeError):
        print("Metric not found or invalid, exiting...")
        sys.exit(1)


def run():
    print("Starting Process...")
    run_frontend(sys.argv[1], sys.argv[6], sys.argv[2])
    f = None
    try:
        f = sys.argv[6].split(".")[0]
    except ValueError:
        print("Bad File")
        sys.exit(1)
    if f is None:
        print("Error")
        sys.exit(1)
    functions, packed_params = run_packer(sys.argv[3], f+".json")

    print()
    for func in functions:
        debug_print_function(func)
    debug_print_packed_params(packed_params)

    new_f = f+"-updated"+sys.argv[6].split(".")[1]

    run_reconstructor(sys.argv[4], new_f, functions, packed_params)
    run_metrics(sys.argv[5], new_f, functions, packed_params)


if __name__ == "__main__":
    run()
