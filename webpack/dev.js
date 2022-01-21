
const merge = require("webpack-merge");
const base = require("./base");

module.exports = merge(base, {
  mode: "development",
  output: {
    publicPath: "/static/"
  },
  watchOptions: {
    aggregateTimeout: 300,
    poll: 1000
  }
});