/**
 * 首页背景：历代名帖。
 *
 * 每次进入站点随机取一幅，经重度虚化后作为「纸背」——只留笔墨与纸张的气韵，
 * 不干扰正文阅读。全部取自维基共享资源（Wikimedia Commons）的公有领域扫描件／拓本，
 * `source` 指向该文件的说明页，与正文「字形图可点击跳转来源」的做法一致。
 *
 * 由 tools/fetch_backdrops.py 生成同名清单 data/backdrops.json；
 * 如需增删，改脚本里的 WORKS 列表后重跑，再把这里同步（内容不多，手写亦可）。
 */

export interface Backdrop {
  key: string
  /** 作品名 */
  name: string
  /** 书家 */
  artist: string
  /** 时代 */
  period: string
  /** 书体 */
  script: string
  /** 相对路径（base: './'，部署在子路径下亦可用） */
  src: string
  /** 原图为深色拓本，展示时已反白为墨稿；此处如实记录该处理 */
  inverted?: boolean
  /** 该图在维基共享资源的说明页 */
  source: string
}

export const BACKDROPS: Backdrop[] = [
  {
    key: 'lanting',
    name: '蘭亭集序（馮承素摹本）',
    artist: '王羲之',
    period: '東晉',
    script: '行書',
    src: 'backdrops/lanting.jpg',
    source: 'https://commons.wikimedia.org/wiki/File:Lantingji_Xu_%E8%98%AD%E4%BA%AD%E5%BA%8F_(cropped).png',
  },
  {
    key: 'jizhiwengao',
    name: '祭姪文稿',
    artist: '顏真卿',
    period: '唐',
    script: '行書',
    src: 'backdrops/jizhiwengao.jpg',
    source: 'https://commons.wikimedia.org/wiki/File:%E5%94%90%E9%A1%8F%E7%9C%9F%E5%8D%BF%E7%A5%AD%E5%A7%AA%E6%96%87%E7%A8%BF_%E5%8D%B7.png',
  },
  {
    key: 'zixutie',
    name: '自敘帖',
    artist: '懷素',
    period: '唐',
    script: '草書',
    src: 'backdrops/zixutie.jpg',
    source: 'https://commons.wikimedia.org/wiki/File:%E5%94%90%E6%87%B7%E7%B4%A0%E8%87%AA%E6%95%98%E5%B8%96_%E5%8D%B7.png',
  },
  {
    key: 'jiuchenggong',
    name: '九成宮醴泉銘',
    artist: '歐陽詢',
    period: '唐',
    script: '楷書',
    src: 'backdrops/jiuchenggong.jpg',
    source: 'https://commons.wikimedia.org/wiki/File:%E5%AE%8B%E6%8B%93%E4%B9%9D%E6%88%90%E5%AE%AB%E9%86%B4%E6%B3%89%E9%93%AD%E5%86%8C_7.jpg',
  },
  {
    key: 'duobaota',
    name: '多寶塔碑',
    artist: '顏真卿',
    period: '唐',
    script: '楷書',
    src: 'backdrops/duobaota.jpg',
    source: 'https://commons.wikimedia.org/wiki/File:%E5%A4%9A%E5%AE%9D%E5%A1%94%E7%A2%91.%E5%94%90.%E9%A2%9C%E7%9C%9F%E5%8D%BF.%E4%B9%A6.%E6%B8%85%E4%B8%AD%E6%99%9A%E6%9C%9F%E6%8B%93%E7%89%87.%E4%B8%9C%E4%BA%AC%E5%9B%BD%E7%AB%8B%E5%8D%9A%E7%89%A9%E9%A6%86%E8%97%8F.jpg',
  },
  {
    key: 'caoquanbei',
    name: '曹全碑',
    artist: '佚名',
    period: '東漢',
    script: '隸書',
    src: 'backdrops/caoquanbei.jpg',
    inverted: true,
    source: 'https://commons.wikimedia.org/wiki/File:%E6%9B%B9%E5%85%A8%E7%A2%91.jpg',
  },
  {
    key: 'shusutie',
    name: '蜀素帖',
    artist: '米芾',
    period: '北宋',
    script: '行書',
    src: 'backdrops/shusutie.jpg',
    source: 'https://commons.wikimedia.org/wiki/File:%E5%AE%8B%E7%B1%B3%E8%8A%BE%E8%9C%80%E7%B4%A0%E5%B8%96_%E5%8D%B7.png',
  },
]

/** 本次访问随机挑一幅（每个页面加载只取一次） */
export function pickBackdrop(): Backdrop {
  return BACKDROPS[Math.floor(Math.random() * BACKDROPS.length)]
}
