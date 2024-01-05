// index.js
// 引入相关方法
const {getCoins,getYaos,getGuaRes,getGuaAns} = require('../../utils/guaRelated.js');
const {toastFail} = require('../../utils/common.js');

Page({
  data: {
    lym_visible: false,
    lyd_visible: false
  },
  onLoad() {
    wx.login({
      success: (res) => {
        console.log(res)
      },
    })
  },
  toBeContinue() {
    toastFail('#toBeContinue','作者还在学习业务逻辑...')
  },
  userInfo(detail) {
    console.log(detail)
  },
  showLym() {
    let page_obj = this;
    page_obj.setData({lym_visible:!page_obj.data.lym_visible});
  },
  returnHome() {
    let page_obj = this;
    let page_data = page_obj.data;
    Object.keys(page_data).forEach((key)=>{
      if (/visible/i.test(key)) {page_obj.setData({[key]:false})}
    })
    console.log(page_data)
  },
  liuyaoInput(e) {
    let page_obj = this;
    // console.log(e.detail.value)
    page_obj.setData({ly_input: e.detail.value});
  },
  async liuyaoAsk() {
    let page_obj = this;
    let coin_res = getCoins(18);
    page_obj.setData({coin_res:coin_res})
    // 切换页面
    page_obj.setData({lyd_visible:true,lym_visible:false})
    await getGuaRes('oIqaO678xkSZgf1Aw1Icjd0F0Nes',coin_res).then(
      (res)=>{
        delete res.data.code;
        page_obj.setData({
          gua_res:res.data,
          yao_res: getYaos(res.data.first_yao.concat(res.data.second_yao))
        })
      });
    let page_data = page_obj.data
    await getGuaAns('oIqaO678xkSZgf1Aw1Icjd0F0Nes',page_data.yao_res,page_data.gua_res.gua_symbol,page_data.ly_input).then(
      (res)=>{
        console.log(res.data)
      }
    )
  }
})