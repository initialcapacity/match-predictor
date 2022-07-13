import {Store} from 'redux';
import {AppState, stateStore} from '../../App/StateStore';
import {fireEvent, render} from '@testing-library/react';
import {TestAppContext} from '../../TestSupport/TestAppContext';
import {forecastRequestState} from '../../Teams/ForecastRequestState';
import ScenarioForm from '../ScenarioForm';

describe('ScenarioForm', () => {
    let store: Store<AppState>;

    beforeEach(() => {
        store = stateStore.create();
    });

    test('ScenarioForm not started', () => {
        store.dispatch(forecastRequestState.setModel({name: 'chicken', predicts_in_progress: false}));

        const page = render(<TestAppContext store={store}>
            <ScenarioForm/>
        </TestAppContext>);


        expect(page.queryByLabelText('Home goals')).toBeNull();
    });

    test('ScenarioForm in progress', () => {
        store.dispatch(forecastRequestState.setInProgress({minutesElapsed: 1, homeGoals: 2, awayGoals: 3}));
        store.dispatch(forecastRequestState.setModel({name: 'pickles', predicts_in_progress: true}));

        const page = render(<TestAppContext store={store}>
            <ScenarioForm/>
        </TestAppContext>);

        expect(page.getByLabelText('minutes elapsed', {selector: 'input'})).toHaveValue(1);
        expect(page.getByLabelText('home goals', {selector: 'input'})).toHaveValue(2);
        expect(page.getByLabelText('away goals', {selector: 'input'})).toHaveValue(3);
    });

    test('ScenarioForm in progress edit', () => {
        store.dispatch(forecastRequestState.setInProgress({minutesElapsed: 1, homeGoals: 2, awayGoals: 3}));
        store.dispatch(forecastRequestState.setModel({name: 'pickles', predicts_in_progress: true}));

        const page = render(<TestAppContext store={store}>
            <ScenarioForm/>
        </TestAppContext>);

        fireEvent.change(page.getByLabelText('minutes elapsed', {selector: 'input'}), {target: {value: '7'}});
        fireEvent.change(page.getByLabelText('home goals', {selector: 'input'}), {target: {value: '8'}});
        fireEvent.change(page.getByLabelText('away goals', {selector: 'input'}), {target: {value: '9'}});

        expect(store.getState().forecastRequest.matchStatus).toEqual({
            type: 'in progress',
            minutesElapsed: 7,
            homeGoals: 8,
            awayGoals: 9,
        });
    });
});
