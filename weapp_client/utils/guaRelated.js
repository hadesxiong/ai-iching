// 引入相关内容
const {baseUrl,number_dict} = require('./config.js');
const {requestSync} = require('./common.js');

// 获取0/1的硬币结果
const getCoins = function(length) {
  return Array.from({ length }, () => Math.floor(Math.random() * 2)).join("");
}

// 投币结果格式化
const formatCoins = function(str) {
  const symbols = Array.from(str).map((char)=>{
    return char == '0' ? '背':'字'
  })
  return symbols.join('')
}

// 信息格式化
const formatMsg = function(coin_res,gua_res) {
  const symbol_str = formatCoins(coin_res)
  const gua_arr = gua_res.first_yao.concat(gua_res.second_yao)
  let yaoMsg_arr = []
  for (let i=0;i<6;i++) {
    yaoMsg_arr.push(number_dict[i]+'为:'+symbol_str.slice(i,i+3)+',为'+gua_arr[i])
  }
  let guaMsg_arr = ['首卦为'+gua_res.first_gua,'次卦为'+gua_res.second_gua]
  return {yao_msg:yaoMsg_arr,gua_msg:guaMsg_arr}
}


// 获取六爻结果并进行处理
const getYaos = function(yaos) {
  // console.log(yaos)
  const yao_array = yaos.map((ele)=>(ele === '阴'?0:1));
  return yao_array.join('');
}

// 获取硬币对应的卦象结果
const getGuaRes = function(openid,coins) {
  const req_url = baseUrl + '/api/liuyao/getGuaRes';
  const req_params = {coin:coins};
  const req_headers = {Userid:openid};
  return requestSync(req_url,req_params,req_headers,'GET').then(
    (res)=>{return res;}
  ).catch(
    (error)=>{throw error;}
  )
}

// 获取文心一言的解答
const getGuaAns = function(openid,yao,gua,ques) {
  const req_url = baseUrl + '/api/liuyao/getLiuYaoRes';
  const req_data = {q:ques,yao:yao,gua:gua};
  const req_headers = {Userid:openid};
  return requestSync(req_url,req_data,req_headers,'POST').then(
    (res)=>{return res;}
  ).catch(
    (error)=>{throw error;}
  )
}

// 获取历史卜卦记录
const getGuaRec = function(openid,args) {
  const req_url = baseUrl + '/api/liuyao/getGuaRec';
  const req_data = args;
  const req_headers = {Userid:openid};
  return requestSync(req_url,req_data,req_headers,'GET').then(
    (res)=>{return res;}
  ).catch(
    (error)=>{throw error;}
  )
}

module.exports = {
  getCoins: getCoins,
  formatCoins: formatCoins,
  formatMsg: formatMsg,
  getYaos: getYaos,
  getGuaRes: getGuaRes,
  getGuaAns: getGuaAns,
  getGuaRec: getGuaRec
}