.PHONY: deliverables check test-package

deliverables:
	python3 package_deliverables.py

check:
	python3 package_deliverables.py --check

test-package:
	python3 -m unittest discover -s tests -p 'test_*.py'
