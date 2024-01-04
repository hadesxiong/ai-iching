// 引入相关内容
const {gua_dict, number_dict} = require('./config.js');

const getCoins = function(length) {
  return Array.from({ length }, () => Math.floor(Math.random() * 2)).join("");
}


module.exports = {
  getCoins: getCoins
}