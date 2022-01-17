import {defineConfig} from 'vite';
import react from '@vitejs/plugin-react';
import eslintPlugin from 'vite-plugin-eslint';

const backendPort = parseInt(process.env.BACKEND_PORT) || 5001;

export default defineConfig({
    plugins: [
        react(),
        eslintPlugin({throwOnWarning: true, throwOnError: true})
    ],
    server: {
        port: parseInt(process.env.PORT) || 3001,
        proxy: {
            '/api': {
                target: `http://localhost:${backendPort}`,
                rewrite: path => path.replace(/^\/api/, '')
            }
        },
    }
});
