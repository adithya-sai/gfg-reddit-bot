all: pipzip functions

pipzip:
	cd package && zip -r9 -q ${TRAVIS_BUILD_DIR}/function.zip .

functions: refresh_fixtures post_thread calculate_score collect_predictions get_result reset_counter
	
refresh_fixtures: pipzip
	cp function.zip src/code.zip
	./deploy/upload.sh -d code.zip -f "$@.py praw.ini common" -x refresh-fixtures-func

post_thread: pipzip
	cp function.zip src/code.zip	
	./deploy/upload.sh -d code.zip -f "$@.py praw.ini common thread_format.txt" -x post-gfg-thread

calculate_score: pipzip
	cp function.zip src/code.zip	
	./deploy/upload.sh -d code.zip -f "$@.py google_sheets.py praw.ini credentials.json common" -x calculate-score-func

collect_predictions: pipzip
	cp function.zip src/code.zip	
	./deploy/upload.sh -d code.zip -f "$@.py praw.ini common" -x collect-prediction-func

get_result: pipzip
	cp function.zip src/code.zip	
	./deploy/upload.sh -d code.zip -f "$@.py praw.ini common" -x get-result-func

reset_counter: pipzip
	cp function.zip src/code.zip	
	./deploy/upload.sh -d code.zip -f "$@.py praw.ini common" -x reset-counter-func