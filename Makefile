include ./src/ref
include ./src/Makefile
include ./ref.local
include ~/bin/generic.mk

.PHONY: pkg
DD:=$(shell date +%Y%M%d)

clean:
	TESTDATA=data/noaa/metar/`date +%Y-%m.tar.gz` && test ! -f $$TESTDATA || rm $$TESTDATA 
test-getsample:
	curl -s 'http://weather.aero/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&stationString=KSEA,UNNT&hoursBeforeNow=2' | xpath -q -e '//raw_text/text()'

# publish-production: PKG=$(shell delivery/`ls -1t delivery | head -1`)
publish-production: export REMOTEHOME = metar@localhost:/home/metar/ # TODO test if if works okay
publish-production: export PKG = $(shell echo `pwd`/delivery/`ls -1t delivery | head -1`)
publish-production: pkg
	# export PKG=delivery/`ls -1t delivery | head -1`
	$(MAKE) --directory env/production -e
publish-mirror: export PKG = $(shell echo `pwd`/delivery/`ls -1t delivery | head -1`)
publish-mirror:	export REMOTEFTPHOST = -u metar,metar localhost
publish-mirror: pkg
	# export PKG=delivery/`ls -1t delivery | head -1`
	$(MAKE) --directory env/mirror -e
