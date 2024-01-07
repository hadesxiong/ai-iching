// index.js
// 引入相关方法
const {getCoins,formatMsg,getYaos,getGuaRes,getGuaAns} = require('../../utils/guaRelated.js');
const {toastFail,toastLoading,toastClear} = require('../../utils/common.js');
const {getLoginCode,getUserInfo,cacheUserInfo,updateAvatar} = require('../../utils/userRelated.js');

// 引入配置
const {baseUrl,hostUrl,aiAvatar} = require('../../utils/config.js');

Page({
  data: {
    hostUrl:hostUrl,
    aiAvatar:aiAvatar,
    lym_visible: false,
    lyd_visible: false
  },
  async onLoad() {
    const page_obj = this;
    try {
      const code = await getLoginCode();
      const user_info = await getUserInfo(code);
      delete user_info.data.code
      cacheUserInfo(user_info.data,page_obj,true)
      console.log(user_info.data)
      if (user_info.data.avatar) {
        page_obj.setData({has_avatar:true})
      }
    } catch (error) {
      console.log('登陆失败',error);
      throw error;
    }
  },
  toBeContinue() {
    toastFail('#toBeContinue','作者还在学习业务逻辑...')
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
  },
  liuyaoInput(e) {
    let page_obj = this;
    page_obj.setData({ly_input: e.detail.value});
  },
  async chooseAvatar(e) {
    let page_obj = this
    let file_path = e.detail.avatarUrl
    console.log(file_path)
    const req_url = baseUrl + '/api/user/avatarUpdate'
    if (!page_obj.data.openid) {
      const code = await getLoginCode();
      const user_info = await getUserInfo(code);
      delete user_info.data.code
      cacheUserInfo(user_info.data,page_obj,true)
    }
    const req_header = {Userid:page_obj.data.openid}
    const res = await updateAvatar(req_url,file_path,req_header);
    console.log(res)
  },
  async liuyaoAsk() {
    let page_obj = this;
    // 判断问题长度是否达标
    if (page_obj.data.ly_input && page_obj.data.ly_input.length >=6) {
      let coin_res = getCoins(18);
      page_obj.setData({coin_res:coin_res})
      // 切换页面
      // 判断是否存在openid,没有则登陆
      if(!page_obj.data.openid) {
        try {
          const code = await getLoginCode();
          const user_info = await getUserInfo(code);
          delete user_info.data.code
          cacheUserInfo(user_info.data,page_obj,true);
        } catch (error) {
          console.log('登陆失败',error);
          throw error;
        }
      }
      // 执行业务逻辑
      toastLoading('#confirmLoading','占卜中...')
      let usr_id = page_obj.data.openid
      await getGuaRes(usr_id,coin_res).then(
        (res)=>{
          delete res.data.code;
          page_obj.setData({
            gua_res:res.data,
            yao_res: getYaos(res.data.first_yao.concat(res.data.second_yao))
          })
          // 打印信息
          const msg_obj = formatMsg(coin_res,page_obj.data.gua_res)
          page_obj.setData({
            yao_msg: msg_obj.yao_msg,
            gua_msg: msg_obj.gua_msg
          })
        }
      )
      await getGuaAns(
        usr_id,
        page_obj.data.yao_res,
        page_obj.data.gua_res.gua_symbol,
        page_obj.data.ly_input
      ).then(
        (res)=>{
          console.log(res)
          page_obj.setData({
            ly_ans:res.data.result,
            ly_ques:page_obj.data.ly_input
          })
          toastClear('#confirmLoading')
          page_obj.setData({
            lyd_visible:true,
            lym_visible:false,
            ly_input:''
          })
        }
      )
    } else {
      toastFail('#inputMsg','问题长度过短...')
    }
  }
})