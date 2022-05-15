import {Action, Reducer} from 'redux';
import {match} from 'ts-pattern';
import {Team} from './TeamsState';
import {Model} from '../Model/ModelsState';


export type Fixture = {
    home: Team,
    away: Team,
    league: string,
}

export type Scenario = {
    minutesElapsed: number
    homeGoals: number
    awayGoals: number
}

export type MatchStatus =
    | { type: 'not started' }
    | { type: 'in progress' } & Scenario

export type ForecastRequest = Fixture & {
    model: Model,
    matchStatus: MatchStatus
}

export type ForecastRequestState = Partial<Fixture> & {
    model?: Model,
    matchStatus: MatchStatus
}

const emptyFixture: ForecastRequestState = {matchStatus: {type: 'not started'}};

type FixtureAction =
    | { type: 'fixture/set home', value: Team }
    | { type: 'fixture/set away', value: Team }
    | { type: 'fixture/set model', value: Model }
    | { type: 'fixture/not started' }
    | { type: 'fixture/in progress', value: Scenario}

const isFixtureAction = (variable: unknown): variable is FixtureAction =>
    (variable as FixtureAction).type.startsWith('fixture/');

const setHome = (value: Team): FixtureAction =>
    ({type: 'fixture/set home', value});

const setAway = (value: Team): FixtureAction =>
    ({type: 'fixture/set away', value});

const setModel = (value: Model): FixtureAction =>
    ({type: 'fixture/set model', value});

const setNotStarted: FixtureAction = { type: 'fixture/not started' };

const setInProgress = (value: Scenario): FixtureAction =>
    ({type: 'fixture/in progress', value});

const reducer: Reducer<ForecastRequestState, Action> = (state = emptyFixture, action: Action): ForecastRequestState => {
    if (!isFixtureAction(action)) return state;

    return match(action)
        .with({type: 'fixture/set home'}, ({value}): ForecastRequestState =>
            ({...state, home: value})
        )
        .with({type: 'fixture/set away'}, ({value}): ForecastRequestState =>
            ({...state, away: value})
        )
        .with({type: 'fixture/set model'}, ({value}): ForecastRequestState =>
            ({...state, model: value})
        )
        .with({type: 'fixture/not started'}, (): ForecastRequestState =>
            ({...state, matchStatus: {type: 'not started'}})
        )
        .with({type: 'fixture/in progress'}, ({value}): ForecastRequestState =>
            ({...state, matchStatus: {type: 'in progress', ...value}})
        )
        .exhaustive();
};

export const forecastRequestState = {
    setHome,
    setAway,
    setModel,
    setNotStarted,
    setInProgress,
    reducer,
};
