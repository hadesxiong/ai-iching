// 引入相关内容
const {baseUrl} = require('./config.js');
const {requestSync} = require('./common.js');

// 获取登陆凭证
const getLoginCode = function() {
  return new Promise((resolve,reject)=>{
    wx.login({
      success:(res)=>{
        if (res.code) { resolve (res.code) }
        else {reject (new Error('login fail' + res.errMsg))}
      },
      fail: (res)=>{reject (new Error('wx.login api fail.'))}
    })
  })
}

// 获取用户信息
const getUserInfo = function(code) {
  const req_url = baseUrl + '/api/user/userLogin';
  const req_data = {code:code};
  return requestSync(req_url,req_data,'GET').then(
    (res)=>{return res}
  ).catch(
    (error)=>{throw error}
  )
}

// 存储用户信息
const cacheUserInfo = function(user_info,page_obj,local_save=false) {
  for (let key in user_info) {
    page_obj.setData({[key]:user_info[key]})
    if (local_save) {wx.setStorageSync(key, user_info[key])}
  }
}

// 上传头像
const updateAvatar = function(_url,_filePath,_header) {
  return new Promise((resolve,reject)=>{
    wx.uploadFile({
      url:_url,
      filePath:_filePath,
      name:'avatar',
      header:_header,
      success: (res)=>{resolve(res.data)},
      fail:(res)=>{reject(res)}
    })
  })
}

module.exports = {
  getLoginCode:getLoginCode,
  getUserInfo:getUserInfo,
  cacheUserInfo:cacheUserInfo,
  updateAvatar:updateAvatar
}