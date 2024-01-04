// 该文件保留一些默认的配置项

const baseUrl = 'https://server.bearman.xyz/ai_iching'

const gua_dict = {
  '阳阳阳': '乾',
  '阴阴阴': '坤',
  '阴阳阳': '兑',
  '阳阴阳': '震',
  '阳阳阴': '巽',
  '阴阳阴': '坎',
  '阳阴阴': '艮',
  '阴阴阳': '离'
}

const number_dict = {
  0: '初爻',
  1: '二爻',
  2: '三爻',
  3: '四爻',
  4: '五爻',
  5: '六爻',
}

// 导出配置信息

module.exports = {
  baseUrl: baseUrl,
  gua_dict: gua_dict,
  number_dict: number_dict
}