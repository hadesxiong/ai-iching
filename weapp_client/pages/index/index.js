Page({
  data: {
    lym_visible: false,
    ly_input: ''
  },

  onLoad() {
    wx.login({
      success: (res) => {
        console.log(res)
      },
    })
  },
  showLym() {
    let page_obj = this;
    page_obj.setData({lym_visible:!page_obj.data.lym_visible});
  },
  liuyaoInput(e) {
    let page_obj = this;
    console.log(e.detail.value)
    this.setData({ly_input: e.detail.value});
  },
  liuyaoAsk() {
    let page_obj = this;
    console.log(page_obj.data.ly_input);
    let liuyao_q = page_obj.data.ly_input;
    if (liuyao_q.length<=0) {
      console.log('wrong question')
    } else {
      wx.request({
        url: 'https://server.bearman.xyz/ai_iching/api/liuyao/getLiuYaoRes',
        method: 'POST',
        data: {
          q:liuyao_q,
          yao:'100100',
          gua:'离坤'
        },
        header: {
          'Userid':'oIqaO678xkSZgf1Aw1Icjd0F0Nes'
        },
        success(res) {
          console.log(res)
        }
      })
    }
  }
})