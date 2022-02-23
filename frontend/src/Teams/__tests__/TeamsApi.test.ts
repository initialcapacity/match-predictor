import {setupServer} from 'msw/node';
import {rest} from 'msw';
import {teamsApi} from '../TeamsApi';

const server = setupServer();

describe('ForecastApi', () => {
    beforeAll(() => server.listen());
    afterEach(() => server.resetHandlers());
    afterAll(() => server.close());

    test('fetch', async () => {
        server.use(
            rest.get('/api/teams', (req, res, ctx) => {
                return res(ctx.json({
                    teams: ['Chelsea', 'AS Roma'],
                }));
            })
        );

        const result = await teamsApi.fetch();

        expect(result).toEqual(['Chelsea', 'AS Roma']);
    });
});
