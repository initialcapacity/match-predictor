import {AppState, stateStore} from '../App/StateStore';
import {ReactElement, ReactNode} from 'react';
import {Store} from 'redux';
import {Provider} from 'react-redux';

interface TestAppContextProps {
    store?: Store<AppState>,
    children: ReactNode,
}

export const TestAppContext = (props: TestAppContextProps): ReactElement =>
    <Provider store={props.store || stateStore.create()}>
        {props.children}
    </Provider>;
