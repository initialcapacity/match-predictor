import * as schemawax from 'schemawax';
import {http} from '../Http/Http';
import {Team} from './TeamsState';
import {result} from '../Http/Result';

const teamsDecoder: schemawax.Decoder<Team[]> =
    schemawax.object({
        required: {
            teams: schemawax.array(schemawax.object({
                required: {
                    name: schemawax.string,
                    leagues: schemawax.array(schemawax.string),
                }
            }))
        }
    }).andThen((json): Team[] => json.teams);

const noTeams: Team[] =
    [];

const fetch = (): Promise<Team[]> => {
    return http
        .sendRequest('/api/teams', teamsDecoder)
        .then(result.orElse(noTeams));
};

export const teamsApi = {
    fetch,
};
