Page({
  data: {
    need_show:false,
  },

  onLoad() {
    wx.login({
      success: (res) => {
        console.log(res)
      },
    })
  },
  click_liuyao() {
    let page_obj = this;
    page_obj.setData({need_show:true});
    console.log(page_obj.data.need_show)
  }
})