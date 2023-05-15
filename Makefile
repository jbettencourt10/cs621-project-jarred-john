FRONTEND=dummy.FrontendDummy
MAX_PARAMS=10
METRICS=dummy.MetricsDummy
PACKER=dummy.PackerDummy
RECONSTRUCTOR=dummy.ReconstructorDummy


build:
	@src/scripts/build.sh

clean:
	@src/scripts/clean.sh

run:
	@src/scripts/run.sh $(FRONTEND) $(MAX_PARAMS) $(PACKER) $(RECONSTRUCTOR) $(METRICS) $(FILE)