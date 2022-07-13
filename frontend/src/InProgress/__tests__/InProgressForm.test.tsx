import {Store} from 'redux';
import {AppState, stateStore} from '../../App/StateStore';
import {render} from '@testing-library/react';
import {TestAppContext} from '../../TestSupport/TestAppContext';
import InProgressForm from '../InProgressForm';
import {forecastRequestState} from '../../Teams/ForecastRequestState';

describe('InProgressForm', () => {
    let store: Store<AppState>;

    beforeEach(() => {
        store = stateStore.create();
    });

    test('InProgressForm render picker', () => {
        store.dispatch(forecastRequestState.setModel({name: 'chicken', predicts_in_progress: true}));

        const page = render(<TestAppContext store={store}>
            <InProgressForm/>
        </TestAppContext>);


        expect(page.queryByLabelText('In progress')).toBeVisible();
    });

    test('InProgressForm don\'t render picker', () => {
        store.dispatch(forecastRequestState.setInProgress({minutesElapsed: 2, homeGoals: 2, awayGoals: 0}));
        store.dispatch(forecastRequestState.setModel({name: 'pickles', predicts_in_progress: false}));

        const page = render(<TestAppContext store={store}>
            <InProgressForm/>
        </TestAppContext>);

        expect(page.queryByLabelText('In progress')).toBeNull();
        expect(store.getState().forecastRequest.matchStatus.type).toEqual('not started');
    });


    test('InProgressForm check', () => {
        store.dispatch(forecastRequestState.setModel({name: 'chicken', predicts_in_progress: true}));

        const page = render(<TestAppContext store={store}>
            <InProgressForm/>
        </TestAppContext>);


        page.getByLabelText('In progress').click();

        expect(store.getState().forecastRequest.matchStatus).toEqual({
            type: 'in progress',
            awayGoals: 0,
            homeGoals: 0,
            minutesElapsed: 0,
        });

        page.getByLabelText('In progress').click();

        expect(store.getState().forecastRequest.matchStatus).toEqual({
            type: 'not started',
        });
    });
});
