/** @type {import('ts-jest/dist/types').InitialOptionsTsJest} */
module.exports = {
    preset: 'ts-jest',
    testEnvironment: 'jsdom',
    moduleNameMapper: {
        '\\.css$': '<rootDir>/src/TestSupport/AssetStubs.js',
        '\\.svg$': '<rootDir>/src/TestSupport/AssetStubs.js',
    },
    globals: {'ts-jest': {useESM: true, isolatedModules: true}},
    setupFilesAfterEnv: ['<rootDir>/src/TestSupport/GlobalHelpers.js']
};
