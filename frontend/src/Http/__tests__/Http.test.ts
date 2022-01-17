import {setupServer} from 'msw/node';
import {rest} from 'msw';
import {http} from '../Http';
import * as schemawax from 'schemawax';

const server = setupServer();

describe('ForecastApi', () => {
    beforeAll(() => server.listen());
    afterEach(() => server.resetHandlers());
    afterAll(() => server.close());

    const decoder = schemawax.object({
        required: {
            success: schemawax.boolean
        }
    });

    test('success', async () => {
        server.use(rest.get('/success', (req, res, ctx) => res(ctx.json({success: true}))));

        const result = http.sendRequest('success', decoder);

        await expect(result).resolves.toEqual({success: true});
    });

    test('500 error', async () => {
        server.use(rest.get('/error', (req, res, ctx) => res(ctx.status(500), ctx.text('Something went wrong'))));

        const result = http.sendRequest('error', decoder);

        await expect(result).rejects.toEqual('Something went wrong');
    });

    test('unexpected json error', async () => {
        server.use(rest.get('/error', (req, res, ctx) => res(ctx.json({unexpected: 'structure'}))));

        const result = http.sendRequest('error', decoder);

        await expect(result).rejects.toEqual('Unable to deserialize response: {"unexpected":"structure"}');
    });

    test('not json error', async () => {
        server.use(rest.get('/error', (req, res, ctx) => res(ctx.text('not json'))));

        const result = http.sendRequest('error', decoder);

        await expect(result).rejects.toEqual('Unable to deserialize response');
    });
});
