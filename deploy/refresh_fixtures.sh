cd ${TRAVIS_BUILD_DIR}/src
FILE_NAME=refresh_fixtures
zip -r9 $FILE_NAME.zip $FILE_NAME.py praw.ini common
cd ${TRAVIS_BUILD_DIR}/package
zip -r9 ${TRAVIS_BUILD_DIR}/src/$FILE_NAME.zip .
cd ${TRAVIS_BUILD_DIR}/src
aws lambda update-function-code --function-name refresh-fixtures-func --zip-file fileb://$FILE_NAME.zip
rm $FILE_NAME.zip
aws lambda update-function-configuration --function-name refresh-fixtures-func --environment Variables="{GFG_ENV=prod, FOOTBALL_API_KEY=${FOOTBALL_API_KEY}}"