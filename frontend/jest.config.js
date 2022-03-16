/** @type {import('ts-jest/dist/types').InitialOptionsTsJest} */
module.exports = {
    preset: 'ts-jest',
    testEnvironment: 'jsdom',
    moduleNameMapper: {
        '\\.css$': '<rootDir>/src/testSupport/AssetStubs.js',
        '\\.svg$': '<rootDir>/src/testSupport/AssetStubs.js',
    },
    globals: {'ts-jest': {useESM: true, isolatedModules: true}},
    setupFilesAfterEnv: ['<rootDir>/src/testSupport/GlobalHelpers.js']
};
