export PERL5LIB=../../pegex-pm/lib

COMPILE_COMMAND = perl -MPegex::Compiler::Bootstrap -e 'print Pegex::Compiler::Bootstrap->new->compile_file(shift)->combinate->to_yaml'

all: grammar1.py

grammar1.py: grammar1.yaml
	python make_module.py $< > $@
	
grammar1.yaml: grammar1.pgx
	$(COMPILE_COMMAND) $< > $@

clean:
	rm -f grammar*.yaml grammar*.py


