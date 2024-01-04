// 引入相关内容
const {gua_dict, number_dict} = require('./config.js');

const get_3_coins = function() {
  return Array.from({length:3},()=> Math.floor(Math.random()*2));
};

const get_yin_yang = function(coin_result) {

};


module.exports = {
  getCoins: get_3_coins,
}