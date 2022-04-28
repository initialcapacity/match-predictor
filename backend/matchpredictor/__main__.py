import os

from matchpredictor.app import create_app

csv_location = os.environ.get('CSV_LOCATION', 'https://projects.fivethirtyeight.com/soccer-api/club/spi_matches.csv')
port = os.environ.get('PORT', 5001)

create_app(csv_location, 2023).run(debug=True, host="0.0.0.0", port=int(port))
