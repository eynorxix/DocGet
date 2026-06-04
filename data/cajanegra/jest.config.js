/** @type {import('jest').Config} */
module.exports = {
  testMatch: ['**/modulos/testing/**/*.test.ts'],
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx'],
  moduleNameMapper: {
    '^@/lib/firestore$': '<rootDir>/modulos/testing/__mocks__/firestore-lib.ts',
    '^@/(.*)$': '<rootDir>/src/$1',
    '^@assets/(.*)$': '<rootDir>/assets/$1',
    '^@modulos/(.*)$': '<rootDir>/modulos/$1',
    '^firebase/firestore$': '<rootDir>/modulos/testing/__mocks__/firestore.ts',
    '^react-native$':
      '<rootDir>/modulos/testing/__mocks__/react-native.ts',
  },
  transform: {
    '^.+\\.tsx?$': ['ts-jest', {
      diagnostics: false,
    }],
  },
  transformIgnorePatterns: [],
  testEnvironment: 'node',
};
