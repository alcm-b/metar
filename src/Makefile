-include ./ref

# ---------------------------------------- production 
test-dbimport: db-importstation db-importobservation db-stat

db-init:
	$(MYSQL_CMD) -e "CREATE USER 'alf'@'localhost' IDENTIFIED BY '1'; GRANT ALL PRIVILEGES ON metar.* to 'alf'@'%' IDENTIFIED BY '1';"
	/usr/bin/mysql_tzinfo_to_sql /usr/share/zoneinfo | $(MYSQL_CMD) -u root mysql
	mysql -p1 metar < sql/metar_schema.sql
db-stat:
	$(MYSQL_CMD) -e "SELECT 'observation' parameter, COUNT(*) value FROM observation \
					UNION SELECT 'station', COUNT(*) FROM station \
					UNION SELECT 'obs start date', MIN(time) FROM observation \
					UNION SELECT 'obs end   date', MAX(time) FROM observation \
					" metar
db-testobservation:
	time $(MYSQL_CMD) -e "SELECT time, temperature as temp, REPEAT('=', temperature), \
		wind_speed AS wind, REPEAT('=', wind_speed) AS wind_speed \
		FROM observation WHERE code='UNNT' AND date(time) = '2011-07-04'" metar

download-station:
	mkdir -p `dirname $(NSDSTATIONS)`
	wget -O $(NSDSTATIONS) http://weather.noaa.gov/data/nsd_bbsss.txt

db-importstation: STATIONS=$(LOCALHOME)/data/stations/station.txt
db-importstation:
	cat $(NSDSTATIONS) | cut -d\; -f 1,2,3,8,9 | perl -pe 's/;//; s/-/./g ; s/\b([0-9.]+)[SW]/-$$1/g; s/(?<=[\d.])[NE]//g' | tr ';' '\t' > $(STATIONS) 
	$(MYSQL_CMD) -e "SET autocommit=0; SET foreign_key_checks=0; LOAD DATA INFILE '$(STATIONS)' INTO TABLE station; COMMIT; SHOW WARNINGS;SET foreign_key_checks=1;" metar 

db-importobservation: OBS_DATE=2011-07-04 
db-importobservation: OBS_DUMP=/tmp/observation.txt
db-importobservation:
	# TODO add logging
# OBS_DUMP _should_be_ absolute path - it is LOAD DATA INFILE requirement
	mkdir -p `dirname $(OBS_DUMP)`
	for i in $(METARDIR)/$(OBS_DATE); do \
		echo $$i...\
		&& cat $$i/*.TXT | $(APPROOT)/src/lib/decodemetar.py | sort | uniq > $(OBS_DUMP) \
		&& $(MYSQL_CMD) -e "SET autocommit=0; SET foreign_key_checks=0; \
					LOAD DATA INFILE '$(OBS_DUMP)' INTO TABLE observation; \
					COMMIT; SHOW WARNINGS; \
					SET foreign_key_checks=1;" metar \
	; done | tee -a $(APPROOT)/tmp/db-importobservation.log
#slow one: --replace 

# ---------------------------------------- mirror 
noaadump-mirror:
# download METAR data from remote storage
	lftp -e "set ssl:verify-certificate no; mirror -v -X *.zip -X *.tar.gz $(REMOTE_METARDIR) $(METARDIR); bye" $(REMOTEFTPHOST)
noaadump-push:
# put locally stored monthly METAR archives on a remote server (backup)
	lftp -e "set ssl:verify-certificate no; mirror -R -r --dry-run -v -I *.tar.gz $(METARDIR) $(REMOTE_METARDIR); bye" $(REMOTEFTPHOST)
noaadump-cleanup: noaadump-mirror
# being on remote server, delete all METAR-containing directories except those for current month
	lftp -e "set ssl:verify-certificate no; cls -1B ${REMOTE_METARDIR}; bye" ${REMOTEFTPHOST} \
		| perl -ne 'print "$$1-??\n" if /(\d\d\d\d-\d\d)(?:-\d\d\/)/ ; ' \
		| sort -r | uniq | sed -ne '1d; p' \
		| while read a ; do \
			echo lftp -e "set ssl:verify-certificate no; \
						cd public_html/weather/data/metar; \
						glob rm $$a/*TXT ; \
						glob -d rmdir $$a ; bye" $(REMOTEFTPHOST) ; \
		done
