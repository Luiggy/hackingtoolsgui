del "dist\*.*" /s /f /q
del "build\*.*" /s /f /q
python setup.py sdist
python setup.py bdist_wheel
python setup.py build
python -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
