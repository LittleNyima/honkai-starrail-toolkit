.PHONY : build
build: clean
	ffmpeg -i resources/images/logo.jpg resources/images/logo.ico
	python -m pip install .
	pyinstaller -D -i resources/images/logo.ico -w -n StarRailToolkit starrail/entry/gui.py
	cp -r resources dist/StarRailToolkit

.PHONY : clean
clean:
	@rm -f resources/images/logo.ico
	@rm -f StarRailToolkit.spec
	@rm -rf dist/
	@rm -rf build/
	@rm -rf starrail_toolkit.egg-info/

.PHONY : publish
publish: clean
	python -m pip install .
	python setup.py sdist bdist_wheel
	ls dist
	twine upload dist/*
