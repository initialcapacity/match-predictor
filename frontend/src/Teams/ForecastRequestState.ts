import {Action, Reducer} from 'redux';
import {match} from 'ts-pattern';
import {Team} from './TeamsState';
import {Model} from '../Model/ModelsState';


export type Fixture = {
    home: Team,
    away: Team,
    league: string,
}

export type ForecastRequest = Fixture & {model: Model}

export type ForecastRequestState = Partial<ForecastRequest>

const emptyFixture: ForecastRequestState = {};

type FixtureAction =
    | { type: 'fixture/set home', value: Team }
    | { type: 'fixture/set away', value: Team }
    | { type: 'fixture/set model', value: Model }

const isFixtureAction = (variable: unknown): variable is FixtureAction =>
    (variable as FixtureAction).type.startsWith('fixture/');

const setHome = (value: Team): FixtureAction =>
    ({type: 'fixture/set home', value});

const setAway = (value: Team): FixtureAction =>
    ({type: 'fixture/set away', value});

const setModel = (value: Model): FixtureAction =>
    ({type: 'fixture/set model', value});

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
        .exhaustive();
};

export const forecastRequestState = {
    setHome,
    setAway,
    setModel,
    reducer,
};
