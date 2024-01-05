// 引入相关内容
const {baseUrl} = require('./config.js');
const {requestSync} = require('./common.js');

// 获取0/1的硬币结果
const getCoins = function(length) {
  return Array.from({ length }, () => Math.floor(Math.random() * 2)).join("");
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

module.exports = {
  getCoins: getCoins,
  getYaos: getYaos,
  getGuaRes: getGuaRes,
  getGuaAns: getGuaAns
}