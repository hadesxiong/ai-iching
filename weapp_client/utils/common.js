// common.js
// 封装一些通用的方法

// 引入toast方法
import Toast from '@vant/weapp/toast/toast';
// 引入dialog方法
import Dialog from '@vant/weapp/dialog/dialog';

const requestSync = function(_url,_data,_header={},_method,_callcomplete) {
  return new Promise(function(resolve,reject){
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

const toastFail = function(id,tip) {
  Toast.fail({
    message:tip,
    forbidClick: true,
    center:true,
    selector: id,
    duration:1500
  })
}

const toastLoading = function(id,tip) {
  Toast.loading({
    duration:0,
    forbidClick:true,
    message:tip,
    selector:id
  })
}

const toastClear = function(id) {
  Toast.clear({
    selector:id
  })
}

const showDialog = function(user_ques,gua_ans,selector) {
  Dialog.alert({
    title:user_ques,
    message: gua_ans,
    selector:selector
  })
}

module.exports = {
  requestSync: requestSync,
  toastFail: toastFail,
  toastLoading: toastLoading,
  toastClear: toastClear,
  showDialog: showDialog
}