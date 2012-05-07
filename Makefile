include ./src/ref
include ./src/Makefile
include ./ref.local
include ~/bin/generic.mk

.PHONY: pkg
DD:=$(shell date +%Y-%M-%d_%H%M%S)
REMOTEFTPHOST=-u metar,metar localhost

clean:
	TESTDATA=data/noaa/metar/`date +%Y-%m.tar.gz` && test ! -f $$TESTDATA || rm $$TESTDATA 
test-getsample:
	curl -s 'http://weather.aero/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&stationString=KSEA,UNNT&hoursBeforeNow=2' | xpath -q -e '//raw_text/text()'

publish-etl: export REMOTEHOME = metar@localhost:/home/metar/
publish-etl: export PKG = $(shell echo `pwd`/delivery/`ls -1t delivery | head -1`)
publish-etl: pkg
	$(MAKE) --directory env/production -e
publish-crawler: export PKG = $(shell echo `pwd`/delivery/`ls -1t delivery | head -1`)
publish-crawler: export REMOTEFTPHOST := $(REMOTEFTPHOST)
publish-crawler: pkg
	$(MAKE) --directory env/crawler -e
