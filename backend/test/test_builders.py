from matchpredictor.app import AppEnvironment


def build_app_environment(
        csv_location: str = 'https://example.com/some.csv',
        season: int = 2023,
        football_data_api_key: str = 'football-data-key-100',
) -> AppEnvironment:
    return AppEnvironment(csv_location, season, football_data_api_key)