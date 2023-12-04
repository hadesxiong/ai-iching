Page({
  data: {},
  onLoad() {
    wx.login({
      success: (res) => {
        console.log(res)
      },
    })
  }
})