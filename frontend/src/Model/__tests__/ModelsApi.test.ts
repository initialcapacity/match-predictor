import {setupServer} from 'msw/node';
import {rest} from 'msw';
import {modelsApi} from '../ModelsApi';

const server = setupServer();

describe('ModelsApi', () => {

    beforeAll(() => server.listen());
    afterEach(() => server.resetHandlers());
    afterAll(() => server.close());

    test('fetch', async () => {
        server.use(
            rest.get('/api/models', (req, res, ctx) => {
                return res(ctx.json({
                    models: [
                        {name: 'linear regression', predicts_in_progress: false},
                        {name: 'coin flip', predicts_in_progress: true},
                    ],
                }));
            })
        );

        const result = await modelsApi.fetch();

        expect(result).toEqual([
            {name: 'linear regression', predicts_in_progress: false},
            {name: 'coin flip', predicts_in_progress: true},
        ]);
    });

    test('fetch, on error', async () => {
        server.use(
            rest.get('/api/models', (req, res, ctx) => {
                return res(ctx.json({
                    models: {this: 'is wrong'},
                }));
            })
        );

        const result = await modelsApi.fetch();

        expect(result).toEqual([]);
    });
});
