import {setupServer} from 'msw/node';
import {rest} from 'msw';
import {forecastApi} from '../ForecastApi';

const server = setupServer();

describe('ForecastApi', () => {
    beforeAll(() => server.listen());
    afterEach(() => server.resetHandlers());
    afterAll(() => server.close());

    test('fetchFor', async () => {
        let searchParams: URLSearchParams = new URLSearchParams();
        server.use(
            rest.get('/api/forecast/england/2020', (req, res, ctx) => {
                searchParams = req.url.searchParams;
                return res(ctx.json({
                    fixture: {
                        home_team: {name: 'Chelsea'},
                        away_team: {name: 'Brighton'},
                        season: 2020,
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
            season: 2020
        });

        expect(searchParams.get('home_team')).toEqual('Chelsea');
        expect(searchParams.get('away_team')).toEqual('Brighton');
        expect(result).toEqual({
            fixture: {
                home: 'Chelsea',
                away: 'Brighton',
                league: 'england',
                season: 2020
            },
            outcome: 'home'
        });
    });
});
