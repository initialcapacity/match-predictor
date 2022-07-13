import {setupServer} from 'msw/node';
import {rest} from 'msw';
import {forecastApi} from '../ForecastApi';
import {result} from '../../Http/Result';

const server = setupServer();

describe('ForecastApi', () => {
    beforeAll(() => server.listen());
    afterEach(() => server.resetHandlers());
    afterAll(() => server.close());

    test('fetchFor', async () => {
        let receivedSearchParams: URLSearchParams = new URLSearchParams();
        server.use(
            rest.get('/api/forecast', (req, res, ctx) => {
                receivedSearchParams = req.url.searchParams;
                return res(ctx.json({
                    fixture: {
                        home_team: {name: 'Chelsea'},
                        away_team: {name: 'Brighton'},
                        league: 'england',
                    },
                    model_name: 'simulation',
                    outcome: 'home',
                    confidence: null
                }));
            })
        );

        const res = await forecastApi.fetchFor({
            home: {name: 'Chelsea', leagues: ['england']},
            away: {name: 'Brighton', leagues: ['england']},
            league: 'england',
            model: {name: 'simulation', predicts_in_progress: false},
            matchStatus: {type: 'not started'}
        });

        expect(receivedSearchParams.get('home_name')).toEqual('Chelsea');
        expect(receivedSearchParams.get('away_name')).toEqual('Brighton');
        expect(receivedSearchParams.get('league')).toEqual('england');
        expect(res).toEqual(result.ok({
            fixture: {
                home: {name: 'Chelsea', leagues: ['england']},
                away: {name: 'Brighton', leagues: ['england']},
                league: 'england',
            },
            model_name: 'simulation',
            outcome: 'home'
        }));
    });

    test('fetchFor with confidence', async () => {
        server.use(
            rest.get('/api/forecast', (req, res, ctx) => {
                return res(ctx.json({
                    fixture: {
                        home_team: {name: 'Chelsea'},
                        away_team: {name: 'Brighton'},
                        league: 'england',
                    },
                    model_name: 'simulation',
                    outcome: 'home',
                    confidence: .43,
                }));
            })
        );

        const res = await forecastApi.fetchFor({
            home: {name: 'Chelsea', leagues: ['england']},
            away: {name: 'Brighton', leagues: ['england']},
            league: 'england',
            model: {name: 'simulation', predicts_in_progress: false},
            matchStatus: {type: 'not started'}
        });

        expect(res).toEqual(result.ok({
            fixture: {
                home: {name: 'Chelsea', leagues: ['england']},
                away: {name: 'Brighton', leagues: ['england']},
                league: 'england',
            },
            model_name: 'simulation',
            outcome: 'home',
            confidence: .43,
        }));
    });

    test('fetchFor in progress', async () => {
        server.use(
            rest.get('/api/forecast-in-progress', (req, res, ctx) => {
                return res(ctx.json({
                    fixture: {
                        home_team: {name: 'Chelsea'},
                        away_team: {name: 'Brighton'},
                        league: 'england',
                    },
                    model_name: 'simulation',
                    outcome: 'home',
                    confidence: .43,
                }));
            })
        );

        const res = await forecastApi.fetchFor({
            home: {name: 'Chelsea', leagues: ['england']},
            away: {name: 'Brighton', leagues: ['england']},
            league: 'england',
            model: {name: 'simulation', predicts_in_progress: true},
            matchStatus: {
                type: 'in progress',
                minutesElapsed: 30,
                homeGoals: 1,
                awayGoals: 2,
            }
        });

        expect(res).toEqual(result.ok({
            fixture: {
                home: {name: 'Chelsea', leagues: ['england']},
                away: {name: 'Brighton', leagues: ['england']},
                league: 'england',
            },
            model_name: 'simulation',
            outcome: 'home',
            confidence: .43,
        }));
    });
});
