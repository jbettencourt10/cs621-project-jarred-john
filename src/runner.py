import sys
import importlib


def run_frontend(frontend, filename, max_params):
    try:
        module_class_pair = frontend.split(".")
        if len(module_class_pair) != 2:
            raise ValueError
        frontend = importlib.import_module("modules.frontends."+module_class_pair[0])
        _FrontendClass = getattr(frontend, module_class_pair[1])
        frontend_obj = _FrontendClass(filename, int(max_params))
        frontend_obj.parse()

    except (ModuleNotFoundError, ValueError, AttributeError):
        print("Frontend not found or invalid, exiting...")
        sys.exit(1)


def run_packer(packer, filename):
    try:
        module_class_pair = packer.split(".")
        if len(module_class_pair) != 2:
            raise ValueError
        packer = importlib.import_module("modules.packers."+module_class_pair[0])
        _PackerClass = getattr(packer, module_class_pair[1])
        packer_obj = _PackerClass(filename)
        packer_obj.minimize()

    except (ModuleNotFoundError, ValueError, AttributeError):
        print("Packer not found or invalid, exiting...")
        sys.exit(1)


def run_visualizer(visualizer, filename):
    try:
        module_class_pair = visualizer.split(".")
        if len(module_class_pair) != 2:
            raise ValueError
        visualizer = importlib.import_module("modules.visualize."+module_class_pair[0])
        _VisualizerClass = getattr(visualizer, module_class_pair[1])
        visual_obj = _VisualizerClass(filename)
        visual_obj.visualize()

    except (ModuleNotFoundError, ValueError, AttributeError):
        print("Packer not found or invalid, exiting...")
        sys.exit(1)


def run():
    print("Starting Process...")

    filename = sys.argv[5] + ".nocomments"

    run_frontend(sys.argv[1], filename, sys.argv[2])

    try:
        filename = filename.split(".")[0]  # Remove extension
    except ValueError:
        print("Bad File")
        sys.exit(1)

    run_packer(sys.argv[3], filename+".json")

    run_visualizer(sys.argv[4], filename+".json")

    print("DONE!")


if __name__ == "__main__":
    run()
