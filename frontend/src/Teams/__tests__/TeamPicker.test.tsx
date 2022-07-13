import {render} from '@testing-library/react';
import {TestAppContext} from '../../TestSupport/TestAppContext';
import TeamPicker from '../TeamPicker';
import {Store} from 'redux';
import {AppState, stateStore} from '../../App/StateStore';
import {teamsState} from '../TeamsState';
import {result} from '../../Http/Result';
import userEvent from '@testing-library/user-event';

describe('TeamPicker', () => {
    let store: Store<AppState>;

    beforeEach(() => {
        store = stateStore.create();

        store.dispatch(teamsState.finishedLoading(result.ok([
            {name: 'Chelsea', leagues: ['england']},
            {name: 'Roma', leagues: ['italy']},
        ])));
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
});
