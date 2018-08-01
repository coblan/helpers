/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId])
/******/ 			return installedModules[moduleId].exports;
/******/
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
/******/ 	// identity function for calling harmony imports with the correct context
/******/ 	__webpack_require__.i = function(value) { return value; };
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
/******/ 	return __webpack_require__(__webpack_require__.s = 1);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var simcms_table_logic = {
    mounted: function mounted() {
        var self = this;
        ex.assign(this.op_funs, {
            edit_page_content: function edit_page_content(kws) {
                var post_data = [{ fun: 'get_cms_content_fields_ctx', name: kws.row.temp_cls }];
                ex.post('/d/ajax/simcms', JSON.stringify(post_data), function (resp) {
                    if (kws.row.content) {
                        var content_row = JSON.parse(kws.row.content);
                    } else {
                        var content_row = {};
                    }

                    var cms_resp_content = resp.get_cms_content_fields_ctx;
                    if (cms_resp_content.tabs) {
                        self.tabgroup.tabs = cms_resp_content.tabs;
                        self.crt_row = kws.row;
                        self.show_tab(self.tabgroup.tabs[0].name);
                    } else {
                        var cms_content_fields_ctx = cms_resp_content.fields_ctx;
                        content_row._director_name = cms_content_fields_ctx.director_name;
                        content_row._page = kws.row.pk;
                        pop_fields_layer(content_row, cms_content_fields_ctx, function (resp) {
                            var new_row = resp.new_row;
                            kws.row.content = JSON.stringify(new_row);
                            //var crt_row=ex.findone(self.rows,{pk:kws.row.pk})
                            //crt_row.content=JSON.stringify(new_row)
                        });
                    }
                });
            }
        });
    }

};
window.simcms_table_logic = simcms_table_logic;

/***/ }),
/* 1 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var _simcms_table_logic = __webpack_require__(0);

var simcms_table_logic = _interopRequireWildcard(_simcms_table_logic);

function _interopRequireWildcard(obj) { if (obj && obj.__esModule) { return obj; } else { var newObj = {}; if (obj != null) { for (var key in obj) { if (Object.prototype.hasOwnProperty.call(obj, key)) newObj[key] = obj[key]; } } newObj.default = obj; return newObj; } }

/***/ })
/******/ ]);