import * as schemawax from 'schemawax';
import {http} from '../Http/Http';

const teamsDecoder: schemawax.Decoder<string[]> =
    schemawax.object({
        required: {
            teams: schemawax.array(schemawax.string)
        }
    }).andThen((json): string[] => json.teams);

const fetch = (): Promise<string[]> => {
    return http.sendRequest('/api/teams', teamsDecoder);
};

export const teamsApi = {
    fetch,
};
