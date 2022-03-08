import {setupServer} from 'msw/node';
import {rest} from 'msw';
import {teamsApi} from '../TeamsApi';

const server = setupServer();

describe('TeamsApi', () => {
    beforeAll(() => server.listen());
    afterEach(() => server.resetHandlers());
    afterAll(() => server.close());

    test('fetch', async () => {
        server.use(
            rest.get('/api/teams', (req, res, ctx) => {
                return res(ctx.json({
                    teams: [{name: 'Chelsea', leagues: ['england']}, {name: 'AS Roma', leagues: ['italy']}],
                }));
            })
        );

        const result = await teamsApi.fetch();

        expect(result).toEqual([{name: 'Chelsea', leagues: ['england']}, {name: 'AS Roma', leagues: ['italy']}]);
    });
});
