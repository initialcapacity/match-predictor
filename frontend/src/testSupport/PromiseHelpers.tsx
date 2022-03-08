import {act} from '@testing-library/react';

export const waitForPromise = async (promise: Promise<unknown>) => {
    try {
        await act(async () => {
            await promise;
        });
        // eslint-disable-next-line no-empty
    } catch {
    }
};

export const waitForRefresh = async () => waitForPromise(Promise.resolve());
