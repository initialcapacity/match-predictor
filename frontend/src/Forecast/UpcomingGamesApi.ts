import {Http, http} from '../Http/Http';
import * as schemawax from 'schemawax';
import {Result} from '../Http/Result';

export declare namespace UpcomingGamesApi {
    type UpcomingGame = {
        league: string
        home: string
        away: string
    }
}

const upcomingGameDecoder: schemawax.Decoder<UpcomingGamesApi.UpcomingGame> =
    schemawax.object({
        required: {
            league: schemawax.string,
            home: schemawax.string,
            away: schemawax.string,
        },
    });

const upcomingGameListDecoder: schemawax.Decoder<UpcomingGamesApi.UpcomingGame[]> =
    schemawax
        .object({
            required: {
                games: schemawax.array(upcomingGameDecoder)
            }
        })
        .andThen(json => json.games);

const fetch = async (dateFrom: string): Promise<Result<UpcomingGamesApi.UpcomingGame[], Http.Error>> =>
    http.sendRequest(`/api/upcoming-games/${dateFrom}`, upcomingGameListDecoder);

export const upcomingGamesApi = {
    fetch,
};
