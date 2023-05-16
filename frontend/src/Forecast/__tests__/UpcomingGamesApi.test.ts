import {setupServer} from 'msw/node';
import {rest} from 'msw';
import {upcomingGamesApi} from '../UpcomingGamesApi';
import {result} from '../../Http/Result';

describe('UpcomingGamesApi', function () {
    const server = setupServer();

    beforeAll(() => server.listen());
    afterEach(() => server.resetHandlers());
    afterAll(() => server.close());

    test('fetch', async () => {

        server.use(
            rest.get('/api/upcoming-games', (req, res, ctx) => {
                return res(ctx.json({
                    games: [
                        {
                            league: 'League 1',
                            home: 'Stade Rennais',
                            away: 'FC Lorient',
                        },
                    ],
                }));
            })
        );

        const games = await upcomingGamesApi.fetch();

        expect(games).toEqual(result.ok([
            {
                league: 'League 1',
                home: 'Stade Rennais',
                away: 'FC Lorient',
            },
        ]));
    });
});
