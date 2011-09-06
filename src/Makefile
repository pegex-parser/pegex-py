BASE=../pegex/grammar

all: $(BASE)/pegex.py

$(BASE)/pegex.py: pegex.pgx.yaml grammar.py Makefile
	python grammar.py $< > $@.tmp
	mv $@.tmp $@
