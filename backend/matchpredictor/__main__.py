import os

from matchpredictor.app import create_app, AppEnvironment


def require_env(name: str) -> str:
    value = os.environ.get(name)
    if value is None:
        raise Exception(f"Failed to read {name} from the environment")
    return value


port = os.environ.get('PORT', 5001)

app_environment = AppEnvironment(
    csv_location=os.environ.get('CSV_LOCATION', 'https://projects.fivethirtyeight.com/soccer-api/club/spi_matches.csv'),
    season=2023,
    football_data_api_key=require_env('FOOTBALL_DATA_API_KEY'),
)

create_app(app_environment).run(debug=True, host="0.0.0.0", port=int(port))
