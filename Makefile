# Waktu Makefile

all:
	python2 setup.py build

install:
	python2 setup.py install --root=$(DESTDIR)

clean:
	python2 setup.py clean
	rm -f MANIFEST
	rm -rf build dist
	find . -name '*.pyc' -exec rm {} \;

export camelCAPS='[a-z_][a-zA-Z0-9_]*$$'
export StudlyCaps='[a-zA-Z_][a-zA-Z0-9_]*$$'

check:
	pylint --indent-string="    " --class-rgx=${StudlyCaps} --function-rgx=${camelCAPS} --method-rgx=${camelCAPS} --variable-rgx=${camelCAPS} --argument-rgx=${camelCaps} waktu/waktu waktu/*.py

tarball:
	python2 setup.py sdist

rpm: tarball
	rpmbuild -tb dist/waktu-*.tar.gz
	mv ~/rpmbuild/RPMS/noarch/* dist/
