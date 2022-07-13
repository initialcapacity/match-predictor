import {setupServer} from 'msw/node';
import {rest} from 'msw';
import {http} from '../Http';
import * as schemawax from 'schemawax';
import {result} from '../Result';

const server = setupServer();

describe('Http', () => {

    beforeEach(() => server.listen());
    afterEach(() => server.close());

    const decoder = schemawax.object({required: {success: schemawax.boolean}});

    test('success', async () => {
        server.use(rest.get('/success', (req, res, ctx) => res(ctx.json({success: true}))));

        const res = await http.sendRequest('success', decoder);

        expect(res).toEqual(result.ok({success: true}));
    });

    test('connection error', async () => {
        server.close();

        const res = await http.sendRequest('error', decoder);

        expect(res).toEqual(result.err({name: 'connection error'}));
    });

    test('500 error', async () => {
        server.use(rest.get('/error', (req, res, ctx) => res(ctx.status(500), ctx.text('Something went wrong'))));

        const res = await http.sendRequest('error', decoder);

        expect(res).toEqual(result.err({name: 'server error', message: 'Something went wrong'}));
    });

    test('unexpected json error', async () => {
        server.use(rest.get('/error', (req, res, ctx) => res(ctx.json({unexpected: 'structure'}))));

        const res = await http.sendRequest('error', decoder);

        expect(res).toEqual(result.err({
            name: 'deserialization error',
            json: '{"unexpected":"structure"}'
        }));
    });

    test('not json error', async () => {
        server.use(rest.get('/error', (req, res, ctx) => res(ctx.text('not json'))));

        const res = await http.sendRequest('error', decoder);

        expect(res).toEqual(result.err({name: 'deserialization error'}));
    });
});
