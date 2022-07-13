import {setupServer} from 'msw/node';
import {rest} from 'msw';
import {Team} from '../../Teams/TeamsState';
import {upcomingGamesApi} from '../UpcomingGamesApi';
import {result} from '../../Http/Result';

describe('UpcomingGamesApi', function () {
    const server = setupServer();

    beforeAll(() => server.listen());
    afterEach(() => server.resetHandlers());
    afterAll(() => server.close());

    test('fetch', async () => {

        const stadeRennais: Team = {name: 'Stade Rennais', leagues: ['League 1']};
        const fcLorient: Team = {name: 'FC Lorient', leagues: ['League 1']};

        server.use(
            rest.get('/api/upcoming-games', (req, res, ctx) => {
                return res(ctx.json({
                    games: [
                        {home: stadeRennais, away: fcLorient},
                        {home: fcLorient, away: stadeRennais},
                    ],
                }));
            })
        );

        const games = await upcomingGamesApi.fetch();

        expect(games).toEqual(result.ok([
            {home: stadeRennais, away: fcLorient},
            {home: fcLorient, away: stadeRennais},
        ]));
    });
});
