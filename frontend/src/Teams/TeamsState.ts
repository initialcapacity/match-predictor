import {Action, Reducer} from 'redux';
import {match} from 'ts-pattern';
import {remoteData, RemoteData} from '../Http/RemoteData';
import {Result} from '../Http/Result';


export interface Team {
    name: string;
    country: string;
}

export interface TeamList {
    teams: Team[];
    countries: string[];
}

export type TeamsState = {
    data: RemoteData<TeamList, string>
};

const initialState: TeamsState = {
    data: remoteData.notLoaded()
};

type TeamsAction =
    | { type: 'teams/start loading' }
    | { type: 'teams/finished loading', value: Result<Team[], string> }

const isTeamsAction = (variable: unknown): variable is TeamsAction =>
    (variable as TeamsAction).type.startsWith('teams/');

const startLoading: TeamsAction =
    {type: 'teams/start loading'};

const finishedLoading = (value: Result<Team[], string>): TeamsAction =>
    ({type: 'teams/finished loading', value});

const reducer: Reducer<TeamsState, Action> = (state = initialState, action: Action): TeamsState => {
    if (!isTeamsAction(action)) return state;

    return match(action)
        .with({type: 'teams/start loading'}, (): TeamsState => ({
            data: remoteData.loading()
        }))
        .with({type: 'teams/finished loading'}, ({value}): TeamsState => {
            if (value.isOk) {
                return {
                    data: remoteData.loaded({
                        teams: value.data,
                        countries: Array.from(new Set(value.data.map(t => t.country)))
                    })
                };
            } else {
                return {data: remoteData.failure(value.reason)};
            }
        })
        .exhaustive();
};

export const teamsState = {
    startLoading,
    finishedLoading,
    reducer,
};
