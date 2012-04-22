include ./src/ref
include ./src/Makefile
include ./ref.local
build: clean
	bin/build.sh
-include ~/bin/generic.mk

.PHONY: pkg

-pkg:
	cp -R src/* pkg
	cp bin/run.sh pkg
	# 2do find a better way to create a clean tree
	rm -rf pkg/data
	mkdir -p pkg/data/noaa/metar
	cp conf/metar.conf pkg/conf/noaajob.conf
publish-noaadumper	: -pkg
# upload NOAA METAR dumper to production
# TODO we no more populate 'pkg' dir, git archive is used instead
	echo quit | lftp -e "mirror -R pkg metar" -u ${REMOTEFTPHOST}
clean:
	TESTDATA=data/noaa/metar/`date +%Y-%m.tar.gz` && test ! -f $$TESTDATA || rm $$TESTDATA 
test-getsample:
	curl -s 'http://weather.aero/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&stationString=KSEA,UNNT&hoursBeforeNow=2' | xpath -q -e '//raw_text/text()'

publish: REMOTEHOME=alf@192.168.1.105:/home/alf/export/metar/
publish: pkg
	scp delivery/`ls -1t delivery | head -1` $(REMOTEHOME)
-remote-deploy:
	for i in Makefile scratch/cycle2txt.py ;\
		do rsync -urtv $$i $(REMOTEHOME)$$i ; done
