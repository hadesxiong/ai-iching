// index.js
Page({
  data:{},
  toDialog: function() {
    console.log('112');
    wx.navigateTo({
      url: '/pages/dialog/dialog',
      events: {},
      success: function() {console.log('11')}
    })
  }
})
