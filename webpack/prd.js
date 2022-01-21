const merge = require("webpack-merge");
const real = require("./real");

module.exports = merge(real, {
  output: {
    publicPath: "/cloud-cgi/static/hack/"
  }
});