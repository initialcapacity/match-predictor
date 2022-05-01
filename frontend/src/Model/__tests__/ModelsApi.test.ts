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
                    models: ['linear regression', 'coin flip'],
                }));
            })
        );

        const result = await modelsApi.fetch();

        expect(result).toEqual([{name: 'linear regression'}, {name: 'coin flip'}]);
    });
});
