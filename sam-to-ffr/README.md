## Fill out the FFR
The FFR, or [SF-425](https://www.gsa.gov/forms-library/federal-financial-report), is a form grantees have to fill out and submit at least four times per year. This proof-of-concept demo fills out several of the FFR's fields using data from SAM.gov, where all grant applicants must register before applying for grants.

## How to run this application
This is a Flask app. To run:

> FLASK_APP=app.py flask run

If `which pdftk` returns anything other than `/usr/bin/pdftk`, you'll need to first set the PDFTK_PATH env variable:

> EXPORT PDFTK_PATH='what/was/returned'
