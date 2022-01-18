import {Fixture, Forecast} from './ForecastState';
import * as schemawax from 'schemawax';
import {http} from '../Http/Http';

const forecastDecoder: schemawax.Decoder<Forecast> =
    schemawax.object({
        required: {
            fixture: schemawax.object({
                required: {
                    home_team: schemawax.object({required: {name: schemawax.string}}),
                    away_team: schemawax.object({required: {name: schemawax.string}}),
                    league: schemawax.string,
                }
            }),
            outcome: schemawax.literalUnion('home', 'away', 'draw')
        }
    }).andThen((json): Forecast => ({
        fixture: {
            home: json.fixture.home_team.name,
            away: json.fixture.away_team.name,
            league: json.fixture.league,
        },
        outcome: json.outcome
    }));

const fetchFor = (fixture: Fixture): Promise<Forecast> => {
    const params = new URLSearchParams({
        home_team: fixture.home,
        away_team: fixture.away,
    });

    return http.sendRequest(`/api/forecast/${fixture.league}?${params}`, forecastDecoder);
};

export const forecastApi = {
    fetchFor,
};
