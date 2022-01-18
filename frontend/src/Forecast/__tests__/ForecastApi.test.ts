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
            rest.get('/api/forecast/england', (req, res, ctx) => {
                receivedSearchParams = req.url.searchParams;
                return res(ctx.json({
                    fixture: {
                        home_team: {name: 'Chelsea'},
                        away_team: {name: 'Brighton'},
                        league: 'england',
                    },
                    outcome: 'home'
                }));
            })
        );

        const result = await forecastApi.fetchFor({
            home: 'Chelsea',
            away: 'Brighton',
            league: 'england',
        });

        expect(receivedSearchParams.get('home_team')).toEqual('Chelsea');
        expect(receivedSearchParams.get('away_team')).toEqual('Brighton');
        expect(result).toEqual({
            fixture: {
                home: 'Chelsea',
                away: 'Brighton',
                league: 'england',
            },
            outcome: 'home'
        });
    });
});
