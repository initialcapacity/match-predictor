import {Forecast} from './ForecastState';
import {Fixture} from '../Teams/ForecastRequestState';
import {Team} from '../Teams/TeamsState';

const defaultLeague =
    'League 1';

const defaultTeam: Team = {
    name: 'FC Lorient',
    leagues: [defaultLeague],
};

const defaultFixture: Fixture = {
    away: defaultTeam,
    home: {...defaultTeam, name: 'Stade Rennais'},
    league: defaultLeague,
};

const defaultForecast: Forecast = {
    confidence: 0,
    fixture: defaultFixture,
    model_name: '',
    outcome: 'home',
};

const builder = <Builder>(defaults: Builder) => (args: Partial<Builder> = {}): Builder =>
    ({...defaults, ...args});

export const forecastTestBuilders = {
    team: builder(defaultTeam),
    fixture: builder(defaultFixture),
    forecast: builder(defaultForecast),
};
