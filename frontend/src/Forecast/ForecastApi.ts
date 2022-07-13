import {Forecast} from './ForecastState';
import * as schemawax from 'schemawax';
import {Http, http} from '../Http/Http';
import {Result} from '../Http/Result';
import {ForecastRequest} from '../Teams/ForecastRequestState';

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
            outcome: schemawax.literalUnion('home', 'away', 'draw'),
            model_name: schemawax.string
        },
        optional: {
            confidence: schemawax.nullable(schemawax.number)
        }
    }).andThen((json): Forecast => ({
        fixture: {
            home: {name: json.fixture.home_team.name, leagues: [json.fixture.league]},
            away: {name: json.fixture.away_team.name, leagues: [json.fixture.league]},
            league: json.fixture.league,
        },
        model_name: json.model_name,
        outcome: json.outcome,
        confidence: json.confidence || undefined,
    }));

const fetchFor = (request: ForecastRequest): Promise<Result<Forecast, Http.Error>> => {
    const params = new URLSearchParams({
        home_name: request.home.name,
        away_name: request.away.name,
        league: request.league,
        model_name: request.model.name,
    });

    if (request.matchStatus.type == 'in progress') {
        params.append('home_goals', request.matchStatus.homeGoals.toString());
        params.append('away_goals', request.matchStatus.awayGoals.toString());
        params.append('minutes_elapsed', request.matchStatus.minutesElapsed.toString());

        return http.sendRequest(`/api/forecast-in-progress?${params}`, forecastDecoder);
    } else {
        return http.sendRequest(`/api/forecast?${params}`, forecastDecoder);
    }
};

export const forecastApi = {
    fetchFor,
};
