/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, {
/******/ 				configurable: false,
/******/ 				enumerable: true,
/******/ 				get: getter
/******/ 			});
/******/ 		}
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 0);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var _department = __webpack_require__(1);

window.DepartSelect = _department.DepartSelect;

/***/ }),
/* 1 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
    value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var DepartSelect = exports.DepartSelect = function () {
    function DepartSelect(back_url, root) {
        _classCallCheck(this, DepartSelect);

        this.back_url = back_url;
        this.root = root || { pk: null, name: '公司' };
    }

    _createClass(DepartSelect, [{
        key: 'select',
        value: function select(_callback) {
            ff.load_vue_com({
                url: "/static/organize/organize.pack.js",
                name: 'depart_select',
                label: '选择部门',
                com_html: '<com-depart-browser :url="url" :root="root"></com-depart-browser>',
                data: {
                    url: this.back_url,
                    root: this.root
                },
                callback: function callback(depart) {
                    _callback(depart);
                }
            });
        }
    }]);

    return DepartSelect;
}();

var depart = {
    props: ['url', 'root'],
    data: function data() {
        return {
            parents: [this.root],
            items: [],

            checked: [],
            clip: [],
            depart_back_call: back_ops(this.url)
        };
    },
    computed: {
        par: function par() {
            return this.parents[this.parents.length - 1];
        }
        //root:function(){
        //    return this.parents[0]
        //}
    },
    mounted: function mounted() {
        this.dir_data(this.par);
    },
    methods: {
        dir_data: function dir_data(item) {
            var self = this;
            this.checked = [];
            this.depart_back_call([{ fun: 'dir_data', root: this.root, par: item }], function (resp) {
                self.parents = resp.dir_data.parents;
                self.items = resp.dir_data.items;
            });
        },

        choice_me: function choice_me(item) {
            this.$parent.callback(item);
            mainView.router.back();
        }
    },
    template: '\n        <div class="scroll-wraper">\n\n            <ul style="margin-top: 0.3em;font-size: 1.3em;">\n                <li v-for="par in parents" @click="dir_data(par)" style="display: inline-block;">\n                    <span v-text="par._label"></span>\n                    <span style="display: inline-block;padding-left: 0.3em;padding-right: 0.3em;">\n                        <i class="fa fa-angle-right" aria-hidden="true"></i>\n                    </span>\n\n                </li>\n            </ul>\n            <ul style="margin-left: 1em;font-size:1.1em;list-style:none;">\n                <li v-for="item in items" style="padding: 0.4em;">\n\n                    <span v-text="item._label" @click="dir_data(item)"></span>\n                    <button style="float: right;margin-right: 1.5em;" @click="choice_me(item)">\u9009\u62E9</button>\n                </li>\n            </ul>\n        </div>\n    '

};

Vue.component('com-depart-browser', depart);

/***/ })
/******/ ]);