
install:
	python3 setup.py install --record installed.log

uninstall:
	sudo cat installed.log | sudo xargs rm -rf


.Phony: install uninstall
