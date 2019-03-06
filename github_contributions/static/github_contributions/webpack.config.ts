const path = require('path');

module.exports = {
    entry: {
        home: './src/home/index.ts',
        repositories: './src/repositories/index.ts',
    },
    module: {
      rules: [
        {
          test: /\.tsx?$/,
          use: 'ts-loader',
          exclude: /node_modules/
        }
      ]
    },
    optimization: {
      splitChunks: {
        // include all types of chunks
        chunks: 'all'
      }
    },
    // output: {
    //     filename: 'main.js',
    //     path: path.resolve(__dirname, 'dist')
    // }
};
