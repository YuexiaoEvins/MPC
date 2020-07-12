const path = require('path');
const CompressionWebpackPlugin = require('compression-webpack-plugin')
function resolve (dir) {
  return path.join(__dirname, './', dir)
}
 // 压缩js
const compress = new CompressionWebpackPlugin(
    {
      filename: info => {
        return `${info.path}.gz${info.query}`
      },
      algorithm: 'gzip',
      threshold: 10240,
      test: new RegExp(
          '\\.(' +
          ['js'].join('|') +
          ')$'
      ),
      minRatio: 0.8,
      deleteOriginalAssets: false
    }
)
module.exports = {
  assetsDir: 'assets',
  publicPath: './',
  lintOnSave: process.env.NODE_ENV === 'development', // 是否开启编译时是否不符合eslint提示
  devServer: {
    host: '0.0.0.0',  // 解决在局域网下无法访问
    port: 8080,
    proxy: {
      '/api': {

        target:'http://192.168.91.5:8008/zhifou',
        // target: 'http://192.168.195.9:8234', // 这是登陆注册测试的接口
        // target: 'http://192.168.195.9:8123', // 这是登陆注册测试的接口
        changeOrigin: true,
        pathRewrite: {
          '^/api':''
        }
      }
    },
    before(app, server) {
      app.get(/.*.(js) | .*.*.(js)$/, (req, res, next) => {
        req.url = req.url + '.gz';
        res.set('Content-Encoding', 'gzip');
        next();
      })
    }
  },
  // 压缩代码
  configureWebpack: {
    plugins: [compress]
  },
  // 配置
  chainWebpack: (config)=>{
    // 修复HMR
    // config.resolve.symlinks(true);
    // 配置别名
    config.resolve.alias
        .set('@', resolve('src'))
        .set('assets',resolve('src/assets'))
        .set('components',resolve('src/components'))
        .set('router',resolve('src/router'))
        .set('utils',resolve('src/utils'))
        .set('static',resolve('src/static'))
        .set('store',resolve('src/store'))
        .set('views',resolve('src/views'))
    // 压缩代码
    config.optimization.minimize(true);
    // 分割代码
    // config.optimization.splitChunks({
    //   chunks: 'all'
    // })
    // 用cdn方式引入
    config.externals({
      'vue': 'Vue',
      'vuex': 'Vuex',
      'vue-router': 'VueRouter',
      'mint-ui': 'MINT',  // 需用MINT
      // 'element-ui':'ELEMENT',
      'axios': 'axios'
    })
  },
  // 引入全局变量
  css: {
    extract: true,
    loaderOptions: {
      // pass options to sass-loader
      sass: {
        // @/ is an alias to src/
        // so this assumes you have a file named `src/variables.scss`
        data: `
               @import "@/assets/css/reselem.scss";
               @import "@/assets/css/variable.scss"; 
               @import "@/assets/css/common.scss";
               @import "@/assets/css/mixin.scss";
              `
      }
    }
  }
}
