.PHONY : build
build:
	@rm -rf resources/images logo.ico
	ffmpeg -i resources/images/logo.jpg resources/images/logo.ico
	python3 setup.py install
	pyinstaller -D -i resources/images/logo.ico -w -n StarRailToolkit starrail/entry/gui.py

.PHONY : clean
clean:
	@rm -rf dist/
	@rm -rf build/
	@rm -rf starrail_toolkit.egg-info
