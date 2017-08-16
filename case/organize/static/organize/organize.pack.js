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

var myrequest = _interopRequireWildcard(_department);

function _interopRequireWildcard(obj) { if (obj && obj.__esModule) { return obj; } else { var newObj = {}; if (obj != null) { for (var key in obj) { if (Object.prototype.hasOwnProperty.call(obj, key)) newObj[key] = obj[key]; } } newObj.default = obj; return newObj; } }

window.data = data;

/***/ }),
/* 1 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var depart = {
    props: ['url', 'root'],
    data: function data() {
        return {
            parents: [this.root],
            items: [],

            checked: [],
            clip: []
        };
    },
    computed: {
        par: function par() {
            return this.parents[this.parents.length - 1];
        },
        root: function root() {
            return this.parents[0];
        }
    },
    mounted: function mounted() {
        this.dir_data(this.par);
    },
    methods: {
        dir_data: function dir_data(item) {
            var self = this;
            this.checked = [];
            dp_back_call([{ fun: 'dir_data', root: this.root, par: item }], function (resp) {
                self.parents = resp.dir_data.parents;
                self.items = resp.dir_data.items;
            });
        }
    },
    template: '\n        <div class="scroll-wraper">\n\n            <ul class="breadcrumb">\n                <li v-for="par in parents" @click="dir_data(par)">\n                    <span v-text="par._label"></span>\n                </li>\n            </ul>\n            <ul style="margin-left: 1em;">\n                <li v-for="item in items" class="flex" style="justify-content:space-between;">\n\n                    <span v-text="item._label" @click="dir_data(item)"></span>\n\n                </li>\n            </ul>\n        </div>\n    '

};

Vue.component('com-depart-browser', depart);

/***/ })
/******/ ]);