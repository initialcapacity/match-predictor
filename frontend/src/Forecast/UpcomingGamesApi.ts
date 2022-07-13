import {Http, http} from '../Http/Http';
import * as schemawax from 'schemawax';
import {Result} from '../Http/Result';

export declare namespace UpcomingGamesApi {
    type Team = {
        name: string;
        leagues: string[];
    }

    type UpcomingGame = {
        home: Team
        away: Team
    }
}

const teamDecoder: schemawax.Decoder<UpcomingGamesApi.Team> =
    schemawax.object({
        required: {
            name: schemawax.string,
            leagues: schemawax.array(schemawax.string)
        }
    });

const upcomingGameDecoder: schemawax.Decoder<UpcomingGamesApi.UpcomingGame> =
    schemawax.object({
        required: {
            home: teamDecoder,
            away: teamDecoder
        }
    });

const upcomingGameListDecoder: schemawax.Decoder<UpcomingGamesApi.UpcomingGame[]> =
    schemawax.object({
        required: {
            games: schemawax.array(upcomingGameDecoder)
        }
    }).andThen(json => json.games);

const fetch = async (): Promise<Result<UpcomingGamesApi.UpcomingGame[], Http.Error>> =>
    http.sendRequest('/api/upcoming-games', upcomingGameListDecoder);

export const upcomingGamesApi = {
    fetch,
};
