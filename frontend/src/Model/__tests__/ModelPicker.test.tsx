import {render} from '@testing-library/react';
import {TestAppContext} from '../../TestSupport/TestAppContext';
import ModelPicker from '../ModelPicker';
import {Store} from 'redux';
import {AppState, stateStore} from '../../App/StateStore';
import {modelsState} from '../ModelsState';
import {result} from '../../Http/Result';
import userEvent from '@testing-library/user-event';

describe('ModelPicker', () => {
    let store: Store<AppState>;

    beforeEach(() => {
        store = stateStore.create();

        store.dispatch(modelsState.finishedLoading(result.ok([
            {name: 'linear regression', predicts_in_progress: false},
            {name: 'coin flip', predicts_in_progress: true},
        ])));
    });

    test('pick', () => {
        const page = render(<TestAppContext store={store}>
            <ModelPicker/>
        </TestAppContext>);

        userEvent.selectOptions(page.getByLabelText('model'), 'linear regression');
        expect(store.getState().forecastRequest.model).toEqual({name: 'linear regression', predicts_in_progress: false});

        userEvent.selectOptions(page.getByLabelText('model'), 'coin flip');
        expect(store.getState().forecastRequest.model).toEqual({name: 'coin flip', predicts_in_progress: true});
    });
});
