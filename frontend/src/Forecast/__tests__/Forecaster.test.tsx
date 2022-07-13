import {render, screen} from '@testing-library/react';
import Forecaster from '../Forecaster';
import {AppConfig} from '../../App/AppConfig';
import {TestAppContext} from '../../TestSupport/TestAppContext';

describe('Forecaster', function () {

    test('with upcoming games enabled', () => {
        const upcomingGamesEnabled: AppConfig = {
            enableUpcomingGames: true
        };

        render(
            <TestAppContext appConfig={upcomingGamesEnabled}>
                <Forecaster/>
            </TestAppContext>
        );

        expect(screen.queryByRole('heading', {name: 'Upcoming Games'})).not.toBeNull();
    });

    test('with upcoming games disabled', () => {
        const upcomingGamesDisabled: AppConfig = {
            enableUpcomingGames: false
        };

        render(
            <TestAppContext appConfig={upcomingGamesDisabled}>
                <Forecaster/>
            </TestAppContext>
        );

        expect(screen.queryByRole('heading', {name: 'Upcoming Games'})).toBeNull();
    });
});