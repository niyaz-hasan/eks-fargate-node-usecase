// webpack.config.js
const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');

module.exports = (_env, argv) => {
  const isProd = argv.mode === 'production';

  return {
    entry: './src/index.js',          // ✅ matches your tree
    output: {
      filename: isProd ? '[name].[contenthash].js' : 'bundle.js',
      path: path.resolve(__dirname, 'build'),  // all bundles land in /build
      publicPath: '/'                           // crucial for React-Router
    },

    plugins: [
      new CleanWebpackPlugin(),
      new HtmlWebpackPlugin({
        template: './public/index.html',  // ✅ keeps your own <title> etc.
        inject: 'body'
      })
    ],

    module: {
      rules: [
        {
          test: /\.jsx?$/,
          exclude: /node_modules/,
          use: 'babel-loader'
        }
      ]
    },
    resolve: { extensions: ['.js', '.jsx'] },

    /* Dev server for local hacking ------------------------------------ */
    devServer: {
      static: path.join(__dirname, 'build'),
      port: 3000,
      historyApiFallback: true,      // React-Router refreshes
      proxy: { '/api': 'http://localhost:5000' }  // → Flask backend
    }
  };
};
