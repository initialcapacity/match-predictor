import {defineConfig} from 'vite';
import react from '@vitejs/plugin-react';
import eslintPlugin from 'vite-plugin-eslint';

const tryParseInt = (value: string | undefined): number | undefined => {
    if (value === undefined) {
        return undefined;
    }

    const parseResult = parseInt(value);
    if (isNaN(parseResult)) {
        return undefined;
    }

    return parseResult;
};

const backendPort = tryParseInt(process.env.BACKEND_PORT) ?? 5001;

export default defineConfig({
    plugins: [
        react(),
        eslintPlugin({throwOnWarning: true, throwOnError: true})
    ],
    server: {
        port: tryParseInt(process.env.PORT) ?? 3001,
        proxy: {
            '/api': {
                target: `http://127.0.0.1:${backendPort}`,
                rewrite: path => path.replace(/^\/api/, '')
            }
        },
    }
});
