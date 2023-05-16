class PackerDummy:
    def __init__(self, functions):
        self.functions = functions
        self.packed_params = {}

    def minimize(self):
        print("packer dummy!")
