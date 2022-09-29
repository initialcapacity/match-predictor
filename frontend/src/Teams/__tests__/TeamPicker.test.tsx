import {render} from '@testing-library/react';
import {TestAppContext} from '../../TestSupport/TestAppContext';
import TeamPicker from '../TeamPicker';
import {Store} from 'redux';
import {AppState, stateStore} from '../../App/StateStore';
import {teamsState} from '../TeamsState';
import {result} from '../../Http/Result';
import userEvent from '@testing-library/user-event';
import {forecastRequestState} from '../ForecastRequestState';

describe('TeamPicker', () => {

    let store: Store<AppState>;
    const chelsea = {name: 'Chelsea', leagues: ['england']};
    const sheffield = {name: 'Sheffield', leagues: ['england']};
    const roma = {name: 'Roma', leagues: ['italy']};

    beforeEach(() => {
        store = stateStore.create();

        store.dispatch(teamsState.finishedLoading(result.ok([chelsea, sheffield, roma])));
    });

    test('filter', () => {
        const page = render(<TestAppContext store={store}>
            <TeamPicker side="home"/>
        </TestAppContext>);

        expect(page.queryByRole('option', {name: 'Chelsea'})).toBeNull();
        expect(page.queryByRole('option', {name: 'Roma'})).toBeNull();

        userEvent.selectOptions(page.getByLabelText('league'), 'england');
        expect(page.queryByRole('option', {name: 'Chelsea'})).toBeVisible();
        expect(page.queryByRole('option', {name: 'Roma'})).toBeNull();

        userEvent.selectOptions(page.getByLabelText('league'), 'italy');
        expect(page.queryByRole('option', {name: 'Chelsea'})).toBeNull();
        expect(page.queryByRole('option', {name: 'Roma'})).toBeVisible();
    });

    test('pick home', () => {
        const page = render(<TestAppContext store={store}>
            <TeamPicker side="home"/>
        </TestAppContext>);

        userEvent.selectOptions(page.getByLabelText('league'), 'england');
        userEvent.selectOptions(page.getByLabelText('name'), 'Chelsea');

        expect(store.getState().forecastRequest.home).toEqual({name: 'Chelsea', leagues: ['england']});
    });

    test('pick away', () => {
        const page = render(<TestAppContext store={store}>
            <TeamPicker side="away"/>
        </TestAppContext>);

        userEvent.selectOptions(page.getByLabelText('league'), 'italy');
        userEvent.selectOptions(page.getByLabelText('name'), 'Roma');

        expect(store.getState().forecastRequest.away).toEqual({name: 'Roma', leagues: ['italy']});
    });

    test('disabling selected home team in the away picker', () => {
        store.dispatch(forecastRequestState.setHome(chelsea));

        const page = render(<TestAppContext store={store}>
            <TeamPicker side="away"/>
        </TestAppContext>);

        userEvent.selectOptions(page.getByLabelText('league'), 'england');

        expect(page.getByRole('option', {name: chelsea.name})).toBeDisabled();
        expect(page.getByRole('option', {name: sheffield.name})).toBeEnabled();
    });

    test('disabling selected away team in the home picker', () => {
        store.dispatch(forecastRequestState.setAway(chelsea));

        const page = render(<TestAppContext store={store}>
            <TeamPicker side="home"/>
        </TestAppContext>);

        userEvent.selectOptions(page.getByLabelText('league'), 'england');

        expect(page.getByRole('option', {name: chelsea.name})).toBeDisabled();
        expect(page.getByRole('option', {name: sheffield.name})).toBeEnabled();
    });
});
