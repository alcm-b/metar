CVDOC = cv1
HTMLHEAD = htmlhead.html
HTMLDOC = $(CVDOC).html
export	:
	cat $(HTMLHEAD) > $(HTMLDOC)
	markdown ./$(CVDOC).markdown >> ./$(HTMLDOC)
	echo "</body></html>" >> $(HTMLDOC)
	htmldoc --webpage --header ... --footer  t.1 -f $(CVDOC).pdf $(HTMLDOC)
commit	: export
	git commit -am "* make commit"
	git push bare
view	: export
	w3m $(HTMLDOC)
pull	:
	git pull origin
publish	: pull
	curl -T cv1.html -u xfpublisher1@day-zero.org:cheraderama22 ftp://day-zero.org/
snapshot	: commit
	rm -rf ./branches/2gis
	mkdir -p ./branches/2gis
	git archive 2gis | tar -x -C ./branches/2gis/
