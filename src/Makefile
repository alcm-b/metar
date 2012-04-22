include ./ref

test-dbimport: db-importstation db-importobservation db-stat

db-init:
	$(MYSQL_CMD) -u root -e "CREATE USER 'alf'@'localhost' IDENTIFIED BY '1'; GRANT ALL PRIVILEGES ON metar.* to 'alf'@'%' IDENTIFIED BY '1';"
	/usr/bin/mysql_tzinfo_to_sql /usr/share/zoneinfo | $(MYSQL_CMD) -u root mysql
	mysql -p1 metar < sql/metar_schema.sql
db-stat:
	mysql -p1 -e "SELECT 'observation' parameter, COUNT(*) value FROM observation \
					UNION SELECT 'station', COUNT(*) FROM station \
					UNION SELECT 'obs start date', MIN(time) FROM observation \
					UNION SELECT 'obs end   date', MAX(time) FROM observation \
					" metar
db-testqueries:
	time mysql -p1 -e "SELECT time, temperature as temp, REPEAT('=', temperature), \
		wind_speed AS wind, REPEAT('=', wind_speed) AS wind_speed \
		FROM observation WHERE code='UNNT' AND date(time) = '2011-07-04'" metar

db-importstation: STATIONS=$(LOCALHOME)/data/stations/station.txt
db-importstation:
	cat $(NSDSTATIONS) | cut -d\; -f 1,2,3,8,9 | perl -pe 's/;//; s/-/./g ; s/\b([0-9.]+)[SW]/-$$1/g; s/(?<=[\d.])[NE]//g' | tr ';' '\t' > $(STATIONS) 
	$(MYSQL_CMD) -e "SET autocommit=0; SET foreign_key_checks=0; LOAD DATA INFILE '$(STATIONS)' INTO TABLE station; COMMIT; SHOW WARNINGS;SET foreign_key_checks=1;" metar  \

db-importobservation: OBS_DATE=2011-07-04 
db-importobservation: OBS_DUMP=/opt/alf/metar/test/observation.txt
db-importobservation:
	for i in $(METARDIR)/$(OBS_DATE); do \
		echo $$i...\
		&& cat $$i/*.TXT | ./scratch/cycle2txt.py | sort | uniq > $(OBS_DUMP) \
		&& $(MYSQL_CMD) -e "SET autocommit=0; SET foreign_key_checks=0; LOAD DATA INFILE '$(OBS_DUMP)' INTO TABLE observation; COMMIT; SHOW WARNINGS;SET foreign_key_checks=1;" metar  \
	; done
		#slow one: --replace 

download-station:
	mkdir -p `dirname $(NSDSTATIONS)`
	wget -O $(NSDSTATIONS) http://weather.noaa.gov/data/nsd_bbsss.txt

remote-mirror:
	lftp -e "set ssl:verify-certificate no; mirror -v -X *.zip -X *.tar.gz $(REMOTE_METARDIR) $(METARDIR); bye" $(REMOTEFTPHOST)
remote-updatearchive:
	lftp -e "set ssl:verify-certificate no; mirror -R -r --dry-run -v -I *.tar.gz $(METARDIR) $(REMOTE_METARDIR); bye" $(REMOTEFTPHOST)
remote-cleanup: remote-mirror
	# delete all directories except those for current month
	lftp -e "set ssl:verify-certificate no; cls -1B ${REMOTE_METARDIR}; bye" ${REMOTEFTPHOST} \
		| perl -ne 'print "$$1-??\n" if /(\d\d\d\d-\d\d)(?:-\d\d\/)/ ; ' \
		| sort -r | uniq | sed -ne '1d; p' \
		| while read a ; do echo lftp -e "set ssl:verify-certificate no; cd public_html/weather/data/metar; glob rm $$a/*TXT ; glob -d rmdir $$a ; bye" $(REMOTEFTPHOST) ; done
