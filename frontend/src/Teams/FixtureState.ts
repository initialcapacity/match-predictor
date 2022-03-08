import {Action, Reducer} from 'redux';
import {match} from 'ts-pattern';
import {Team} from './TeamsState';

export type Fixture = {
    home: Team,
    away: Team,
    league: string,
}

export type FixtureState = Partial<Fixture>

const emptyFixture: FixtureState = {};

type FixtureAction =
    | { type: 'fixture/clear' }
    | { type: 'fixture/set home', value: Team }
    | { type: 'fixture/set away', value: Team }

const isFixtureAction = (variable: unknown): variable is FixtureAction =>
    (variable as FixtureAction).type.startsWith('fixture/');

const clear: FixtureAction =
    {type: 'fixture/clear'};

const setHome = (value: Team): FixtureAction =>
    ({type: 'fixture/set home', value});

const setAway = (value: Team): FixtureAction =>
    ({type: 'fixture/set away', value});

const reducer: Reducer<FixtureState, Action> = (state = emptyFixture, action: Action): FixtureState => {
    if (!isFixtureAction(action)) return state;

    return match(action)
        .with({type: 'fixture/clear'}, (): FixtureState => emptyFixture)
        .with({type: 'fixture/set home'}, ({value}): FixtureState =>
            ({...state, home: value})
        )
        .with({type: 'fixture/set away'}, ({value}): FixtureState =>
            ({...state, away: value})
        )
        .exhaustive();
};

export const fixtureState = {
    clear,
    setHome,
    setAway,
    reducer,
};
