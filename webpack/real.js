const TerserPlugin = require("terser-webpack-plugin");
const merge = require("webpack-merge");
const base = require("./base");

module.exports = merge(base, {
  mode: "production",
  optimization: {
    moduleIds: "hashed",
    chunkIds: "size",
    minimizer: [
      new TerserPlugin({
        cache: true,
        parallel: false,
        terserOptions: {
          compress: {
            evaluate: false,
            comparisons: false,
            inline: 2
          },
          mangle: {
            safari10: true
          },
          ecma: 6,
          output: {
            safari10: true,
            comments: false
          }
        },
        exclude: [/\.min\.js$/gi]
      })
    ]
  }
});