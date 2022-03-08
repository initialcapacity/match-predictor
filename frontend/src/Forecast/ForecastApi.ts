import {Forecast} from './ForecastState';
import * as schemawax from 'schemawax';
import {http} from '../Http/Http';
import {Fixture} from '../Teams/FixtureState';

const teamDecoder: schemawax.Decoder<{ name: string }> = schemawax.object({required: {name: schemawax.string}});

const forecastDecoder: schemawax.Decoder<Forecast> =
    schemawax.object({
        required: {
            fixture: schemawax.object({
                required: {
                    home_team: teamDecoder,
                    away_team: teamDecoder,
                    league: schemawax.string,
                }
            }),
            outcome: schemawax.literalUnion('home', 'away', 'draw')
        }
    }).andThen((json): Forecast => ({
        fixture: {
            home: { name: json.fixture.home_team.name, leagues: [json.fixture.league]},
            away: { name: json.fixture.away_team.name, leagues: [json.fixture.league]},
            league: json.fixture.league
        },
        outcome: json.outcome
    }));

const fetchFor = (fixture: Fixture): Promise<Forecast> => {
    const params = new URLSearchParams({
        home_name: fixture.home.name,
        away_name: fixture.away.name,
        league: fixture.league,
    });

    return http.sendRequest(`/api/forecast?${params}`, forecastDecoder);
};

export const forecastApi = {
    fetchFor,
};
