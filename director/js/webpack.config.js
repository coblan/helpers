

var path = require( 'path' );

var webpack = require('D:/coblan/webcode/node_modules/webpack')

//const VueLoaderPlugin = require('D:/coblan/webcode/node_modules/vue-loader/lib/plugin')
const VueLoaderPlugin = require('vue-loader/lib/plugin');
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin
var {CleanWebpackPlugin} = require('clean-webpack-plugin');

var webpack = require('webpack')

module.exports =
{
    //context:__dirname,
    mode:'production', //'development', //
    entry: {
        director:'./director/director.js',
        exfun:'./exfun/main.js'
    },
    output: {
        path:path.resolve(__dirname, '../static/js'),
        filename: '[name].pack.js'
    },
    externals: {
        'vue': 'Vue',
        'vue-router': 'VueRouter',
        'axios': 'axios',
        'element-ui': 'Element',
        'qs': 'Qs'
    },

    watch: true,
    resolve:{
        alias: {
            jb_admin: path.resolve(__dirname,"../../case/jb_admin/js"),
            weblib:'D:/coblan/weblib',
            webcase:'D:/coblan/webcase',
        },
        modules:["D:/coblan/webcode/node_modules"],
    },
    resolveLoader: {
        //moduleExtensions:["D:/coblan/webcode/node_modules"],
        modules: ["D:/coblan/webcode/node_modules"],
        //resolver:["D:/coblan/webcode/node_modules"],
    },
    module: {
        rules: [
            {
                test: /\.vue$/,
                loader: 'vue-loader'
            },
            // {
            //     test: /\.m?js$/,
            //     exclude: /(node_modules|bower_components)/,
            //     use: {
            //         loader: 'babel-loader',
            //         options: {
            //             presets:[
            //                 require.resolve('@babel/preset-env')
            //             ]
            //
            //         }
            //     },
            // },
            {
                test: /\.m?js$/,
                exclude: /(node_modules|bower_components)/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets:[
                            require.resolve('@babel/preset-env')
                        ],
                        plugins: [
                            require.resolve("@babel/plugin-transform-runtime")
                        ]

                    }
                },
            },
            {
                test: /\.scss$/,
                use: [{
                    loader: "style-loader" // creates style nodes from JS strings
                }, {
                    loader: "css-loader" // translates CSS into CommonJS
                }, {
                    loader: "sass-loader" // compiles Sass to CSS
                },{
                    loader: path.resolve('./deepChangeLoader.js'),
                }]
            },
            {
                test: /\.styl$/,
                use: [
                    {
                        loader: "style-loader" // creates style nodes from JS strings
                    },
                    {
                        loader: "css-loader" // translates CSS into CommonJS
                    },
                    {
                        loader: "stylus-loader" // compiles Stylus to CSS
                    }
                ]
            },
            {
                test: /\.less$/,
                use: [{
                    loader: 'style-loader' // creates style nodes from JS strings
                }, {
                    loader: 'css-loader' // translates CSS into CommonJS
                }, {
                    loader: 'less-loader' // compiles Less to CSS
                }]
            }
        ]

    },
    plugins: [
        new VueLoaderPlugin(),
        new CleanWebpackPlugin(),

        //new UglifyJSPlugin()
        //new webpack.DefinePlugin({
        //'process.env.NODE_ENV': JSON.stringify('production'),
        //}),
    ]
}



