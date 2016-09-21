const path = require('path'); // eslint-disable-line
const webpack = require('webpack'); // eslint-disable-line

module.exports = {
  entry: './bundleEntry.js',
  output: { path: `${__dirname}`, filename: './dist/bundle.js' },
  debug: true,
  devtool: 'source-map',
  module: {
    loaders: [
      {
        test: /.jsx?$|.es6$/,
        loader: 'babel-loader',
        exclude: /node_modules/,
        query: {
          presets: ['es2015', 'react'],
        },
      },
    ],
  },
};
