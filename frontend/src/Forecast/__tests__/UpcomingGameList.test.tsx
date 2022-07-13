import {UpcomingGameList} from '../UpcomingGameList';
import {render, screen} from '@testing-library/react';
import {mocked} from 'jest-mock';
import {UpcomingGamesApi, upcomingGamesApi} from '../UpcomingGamesApi';
import {Result, result} from '../../Http/Result';
import {http, Http} from '../../Http/Http';

jest.mock('../UpcomingGamesApi');

describe('UpcomingGameList', () => {

    const chelsea = {name: 'Chelsea', leagues: ['england']};
    const burnley = {name: 'Burnley', leagues: ['england']};
    const sheffield = {name: 'Sheffield', leagues: ['england']};
    const liverpool = {name: 'Liverpool', leagues: ['england']};

    const games: UpcomingGamesApi.UpcomingGame[] = [
        {home: chelsea, away: burnley},
        {home: burnley, away: chelsea},
    ];

    test('loading the list from the backend', async () => {

        const successResult: Result<UpcomingGamesApi.UpcomingGame[], Http.Error> =
            result.ok(games);

        mocked(upcomingGamesApi).fetch.mockImplementation(async () => successResult);

        render(<UpcomingGameList/>);

        const chelseaOccurrences = await screen.findAllByText('Chelsea');
        expect(chelseaOccurrences).toHaveLength(2);

        const burnleyOccurrences = await screen.findAllByText('Burnley');
        expect(burnleyOccurrences).toHaveLength(2);
    });

    test('failing to load the list from the backend', async () => {

        const failureResult: Result<UpcomingGamesApi.UpcomingGame[], Http.Error> =
            result.err(http.connectionError);

        mocked(upcomingGamesApi).fetch.mockImplementation(async () => failureResult);

        render(<UpcomingGameList/>);

        await screen.findByText('There was an error, please try again later.');
    });

    test('refreshing the list', async () => {
        mocked(upcomingGamesApi).fetch.mockImplementation(async () => result.ok(games));

        render(<UpcomingGameList/>);

        const burnleyOccurrences = await screen.findAllByText('Burnley');
        expect(burnleyOccurrences).toHaveLength(2);

        const refreshedGames: UpcomingGamesApi.UpcomingGame[] = [
            {home: sheffield, away: liverpool}
        ];

        mocked(upcomingGamesApi).fetch.mockImplementation(async () => result.ok(refreshedGames));

        screen.getByRole('button', {name: 'Refresh'}).click();

        screen.getByText('Refreshing data...');

        await screen.findByText('Liverpool');
        await screen.findByText('Sheffield');

        expect(screen.queryByText('Burnley')).toBeNull();
        expect(screen.queryByText('Chelsea')).toBeNull();
    });
});
