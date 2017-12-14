const path = require('path'); // eslint-disable-line
const webpack = require('webpack'); // eslint-disable-line

// debug: true,
module.exports = {
  entry: './bundleEntry.js',
  output: { path: `${__dirname}`, filename: './dist/bundle.js' },
  plugins: [
    new webpack.LoaderOptionsPlugin({
      debug: true,
    }),
  ],
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
