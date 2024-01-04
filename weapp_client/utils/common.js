import { CameraComponent } from "XrFrame/kanata/lib/index";
// common.js
// 封装一些通用的方法

const requestSync = function(_url,_data,_header,_method,_callcomplete) {
  return pro_obj = new Promise(function(resolve,reject){
    wx.request({
      url: _url,
      data: _data,
      header: _header,
      method:_method,
      success: function(res) {
        if (res.statusCode == 200) {
          console.log('wx.request() success:200,ok.');
          resolve(res);
        } else {
          console.log('wx.request() success:200,fail');
          reject(res);
        }
      },
      fail: function(res) {
        console.log('wx.request() fail:' + res.statusCode + 'err:' + res.errMsg);
        reject(res);
      },
      complete: function(res) {
        console.log('wx.request() complete');
        if(_callcomplete) {_callcomplete(res)}
      }
    })
  });
}

module.exports = {
  requestSync: requestSync
}