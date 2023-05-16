FRONTEND=dummy.FrontendDummy
MAX_PARAMS=10
PACKER=dummy.PackerDummy
VISUALIZER=dummy.VisualizerDummy


build:
	@src/scripts/build.sh

clean:
	@src/scripts/clean.sh

run:
	@src/scripts/run.sh $(FRONTEND) $(MAX_PARAMS) $(PACKER) $(VISUALIZER) $(FILE)