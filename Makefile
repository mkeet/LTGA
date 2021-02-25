compilejs:
	(cd peers/static && browserify -t reactify -o bundle.js main.js)

watchjs:
	(cd peers/static && watchify -t reactify -o bundle.js main.js)

debug: compilejs
	python run_debug.py
