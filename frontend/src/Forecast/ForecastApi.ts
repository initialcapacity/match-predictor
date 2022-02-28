import {Forecast} from './ForecastState';
import * as schemawax from 'schemawax';
import {http} from '../Http/Http';
import {Fixture} from '../Teams/FixtureState';
import {Team} from '../Teams/TeamsState';

const teamDecoder: schemawax.Decoder<Team> = schemawax.object({required: {name: schemawax.string, country: schemawax.string}});

const forecastDecoder: schemawax.Decoder<Forecast> =
    schemawax.object({
        required: {
            fixture: schemawax.object({
                required: {
                    home_team: teamDecoder,
                    away_team: teamDecoder,
                }
            }),
            outcome: schemawax.literalUnion('home', 'away', 'draw')
        }
    }).andThen((json): Forecast => ({
        fixture: {
            home: json.fixture.home_team,
            away: json.fixture.away_team,
        },
        outcome: json.outcome
    }));

const fetchFor = (fixture: Fixture): Promise<Forecast> => {
    const params = new URLSearchParams({
        home_name: fixture.home.name,
        home_country: fixture.home.country,
        away_name: fixture.away.name,
        away_country: fixture.away.country,
    });

    return http.sendRequest(`/api/forecast?${params}`, forecastDecoder);
};

export const forecastApi = {
    fetchFor,
};
