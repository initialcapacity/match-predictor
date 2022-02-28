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
                        home_team: {name: 'Chelsea', country: 'england'},
                        away_team: {name: 'Brighton', country: 'england'},
                    },
                    outcome: 'home'
                }));
            })
        );

        const result = await forecastApi.fetchFor({
            home: {name: 'Chelsea', country: 'england'},
            away: {name: 'Brighton', country: 'england'},
        });

        expect(receivedSearchParams.get('home_name')).toEqual('Chelsea');
        expect(receivedSearchParams.get('home_country')).toEqual('england');
        expect(receivedSearchParams.get('away_name')).toEqual('Brighton');
        expect(receivedSearchParams.get('away_country')).toEqual('england');
        expect(result).toEqual({
            fixture: {
                home: {name: 'Chelsea', country: 'england'},
                away: {name: 'Brighton', country: 'england'},
            },
            outcome: 'home'
        });
    });
});
