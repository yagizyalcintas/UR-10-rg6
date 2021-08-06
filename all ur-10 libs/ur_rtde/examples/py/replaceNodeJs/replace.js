"use strict";
exports.__esModule = true;
var TM = require("./TM.js")
var map = require("./config.js")
var json_placeholder_replacer_1 = require("json-placeholder-replacer");
var placeHolderReplacer = new json_placeholder_replacer_1.JsonPlaceholderReplacer();

placeHolderReplacer.addVariableMap(map);

var afterReplace = placeHolderReplacer.replace(TM);

console.log(JSON.stringify(afterReplace));
