const path = require('path');

module.exports = {
    entry: {
        home: './src/home/index.ts',
        repositories: './src/repositories/index.ts',
    },
    optimization: {
      splitChunks: {
        // include all types of chunks
        chunks: 'all'
      }
    }
    // output: {
    //     filename: 'main.js',
    //     path: path.resolve(__dirname, 'dist')
    // }
};
