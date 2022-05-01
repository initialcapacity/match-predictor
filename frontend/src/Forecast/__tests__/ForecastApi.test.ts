import {setupServer} from 'msw/node';
import {rest} from 'msw';
import {forecastApi} from '../ForecastApi';

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

        const result = await forecastApi.fetchFor({
            home: {name: 'Chelsea', leagues: ['england']},
            away: {name: 'Brighton', leagues: ['england']},
            league: 'england',
            model: {name: 'simulation'},
        });

        expect(receivedSearchParams.get('home_name')).toEqual('Chelsea');
        expect(receivedSearchParams.get('away_name')).toEqual('Brighton');
        expect(receivedSearchParams.get('league')).toEqual('england');
        expect(result).toEqual({
            fixture: {
                home: {name: 'Chelsea', leagues: ['england']},
                away: {name: 'Brighton', leagues: ['england']},
                league: 'england',
            },
            model: {name: 'simulation'},
            outcome: 'home'
        });
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

        const result = await forecastApi.fetchFor({
            home: {name: 'Chelsea', leagues: ['england']},
            away: {name: 'Brighton', leagues: ['england']},
            league: 'england',
            model: {name: 'simulation'},
        });

        expect(result).toEqual({
            fixture: {
                home: {name: 'Chelsea', leagues: ['england']},
                away: {name: 'Brighton', leagues: ['england']},
                league: 'england',
            },
            model: {name: 'simulation'},
            outcome: 'home',
            confidence: .43,
        });
    });
});
