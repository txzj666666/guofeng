"""
引导式截图加注：给关键帧加 序号 / 箭头 / 文字 气泡
颜色:朱砂红 + 金线 + 米白（与主视觉保持一致）
"""
from PIL import Image, ImageDraw, ImageFont
import os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(ROOT, 'screenshots')

# 关键帧加注方案
# 每一条: (源文件, 多个标注块)
# block: {idx, x, y, w, h, label, sub, arrow (可选: 起点x1,y1, 终点x2,y2)}
ANNOT = [
  # 引导式 16 帧走查
  ('guide-01-cover.png',          [('01', 24, 24, 320, None, '【壹 · 卷轴首页】', '键盘 → 或 数字 1-4 切换页',  None, None, None, None)]),
  ('guide-02-forge-default.png',  [
    ('02', 24, 24, 320, None, '【贰 · 铸剑阁】', '按 → 翻页进入，已加载默认配置', None, None, None, None),
    ('a', 1180, 240, 240, None, '翻页按钮', '点击或键盘', 1190, 250, 1140, 410),
  ]),
  ('guide-03-forge-hero-change.png', [
    ('03', 24, 24, 320, None, '【叁 · 切换名将】', '点击张飞 · 自动选定铁骑兵', None, None, None, None),
    ('a', 1180, 200, 240, None, '已选', '数据保真重算', 1190, 220, 760, 500),
  ]),
  ('guide-04-forge-lvl60-detail.png', [
    ('04', 24, 24, 320, None, '【肆 · 调整等级至 Lv.60】', '明细表实时演算，全部数字可追溯', None, None, None, None),
    ('a', 1180, 80, 240, None, '总银两', '(Lv39 × 6000) × 1.2', 1190, 100, 900, 230),
  ]),
  ('guide-05-forge-path-change.png', [
    ('05', 24, 24, 320, None, '【伍 · 更换修炼路径】', '「行伍历练」· 1500 XP / 日', None, None, None, None),
    ('a', 1180, 80, 240, None, '时日同步', '重新计算修炼月数', 1190, 100, 900, 600),
  ]),
  ('guide-06-gallery-grid.png', [
    ('06', 24, 24, 320, None, '【陆 · 将星图鉴】', '12 名将 · 可筛选 · 可搜索', None, None, None, None),
    ('a', 1180, 600, 240, None, '点击卡片', '展开详细列传', 1190, 620, 950, 760),
  ]),
  ('guide-07-gallery-filter.png', [
    ('07', 24, 24, 320, None, '【柒 · 按朝代筛选】', '点击「秦汉」· 即时过滤', None, None, None, None),
    ('a', 1180, 130, 240, None, '筛选 chip', '44×44px 可点热区', 1190, 150, 250, 170),
  ]),
  ('guide-08-gallery-detail-hanxin.png', [
    ('08', 24, 24, 320, None, '【捌 · 展开韩信列传】', '五维属性条 · 可「以此将铸器」', None, None, None, None),
    ('a', 1180, 480, 240, None, '能力条', '武力 / 智力 / 统率 / 政治 / 魅力', 1190, 500, 600, 540),
  ]),
  ('guide-09-epilogue.png', [
    ('09', 24, 24, 320, None, '【玖 · 终章寄语】', '数字键 4 直跳 · 红日 + 印章收尾', None, None, None, None),
  ]),
  ('guide-10-back-to-cover.png', [
    ('10', 24, 24, 320, None, '【拾 · 由终章返回】', '数字键 1 直跳回首页', None, None, None, None),
  ]),
  ('guide-11-direct-to-gallery.png', [
    ('11', 24, 24, 320, None, '【拾壹 · 直跳图鉴】', '任何位置按 3 直跳', None, None, None, None),
  ]),
  ('guide-12-mobile-cover.png', [
    ('12', 24, 24, 380, None, '【拾贰 · 移动端首页】', 'iPhone 12 · 375px 视口', None, None, None, None),
  ]),
  ('guide-13-mobile-forge.png', [
    ('13', 24, 24, 380, None, '【拾叁 · 移动端铸剑阁】', '2 列将领 · 触控热区 ≥44px', None, None, None, None),
  ]),
  ('guide-14-mobile-gallery.png', [
    ('14', 24, 24, 380, None, '【拾肆 · 移动端图鉴】', '纵向瀑布 · 全可点', None, None, None, None),
  ]),
]

FONT_TITLE = r'C:\Windows\Fonts\simhei.ttf'
FONT_SUB   = r'C:\Windows\Fonts\simsun.ttc'

# 颜色
COL_CINN = (200, 51, 46)
COL_GOLD = (212, 175, 55)
COL_PAPER= (239, 226, 196)
COL_INK  = (7, 6, 10)

def draw_panel(draw, x, y, w, h, alpha_bg=True):
  """画金边 + 暗底 + 圆角面板"""
  r = 8
  if alpha_bg:
    # 暗底
    draw.rounded_rectangle([x, y, x+w, y+h], radius=r, fill=(7,6,10,235))
  # 金边
  draw.rounded_rectangle([x+0.5, y+0.5, x+w-0.5, y+h-0.5], radius=r, outline=COL_GOLD, width=2)
  # 内层虚线
  draw.rounded_rectangle([x+6, y+6, x+w-6, y+h-6], radius=r-2, outline=(212,175,55,160), width=1)

def draw_seq_badge(draw, x, y, n, size=48):
  """序号红色方印"""
  s = size
  # 阴影
  draw.rounded_rectangle([x, y, x+s, y+s], radius=5, fill=(0,0,0,200))
  # 印章红
  draw.rounded_rectangle([x, y, x+s-2, y+s-2], radius=5, fill=COL_CINN)
  # 内白边
  draw.rounded_rectangle([x+3, y+3, x+s-5, y+s-5], radius=3, outline=(255,245,224,180), width=1)
  # 数字（自适应字号）
  try:
    fs = 22 if len(n)==1 else 18
    font = ImageFont.truetype(FONT_TITLE, fs)
    # 垂直居中
    asc, dsc = font.getmetrics()
    th = asc + dsc
    tw = draw.textlength(n, font=font)
    draw.text((x + (s - tw)/2, y + (s - th)/2 - 1), n, font=font, fill=(255,245,224))
  except Exception:
    pass

def draw_arrow(draw, x1, y1, x2, y2, color=COL_GOLD, w=3):
  """贝塞尔曲线 + 箭头 + 起止菱形点"""
  import math
  # 直线
  draw.line([x1, y1, x2, y2], fill=color, width=w)
  # 终点箭头
  ang = math.atan2(y2-y1, x2-x1)
  L = 14
  a1 = (x2 - L*math.cos(ang - math.pi/7), y2 - L*math.sin(ang - math.pi/7))
  a2 = (x2 - L*math.cos(ang + math.pi/7), y2 - L*math.sin(ang + math.pi/7))
  draw.polygon([x2,y2, a1, a2], fill=color)
  # 起点菱形
  s = 6
  draw.polygon([(x1-s,y1),(x1,y1-s),(x1+s,y1),(x1,y1+s)], fill=color)

def annotate_one(src, blocks):
  p = os.path.join(SHOTS, src)
  if not os.path.exists(p): return False
  img = Image.open(p).convert('RGBA')
  W, H = img.size
  overlay = Image.new('RGBA', img.size, (0,0,0,0))
  d = ImageDraw.Draw(overlay)

  # 暗角遮罩
  mask = Image.new('L', img.size, 0)
  md = ImageDraw.Draw(mask)
  # 不加整体暗角(只是为了让气泡突出,给气泡底板画半透明黑即可)

  for blk in blocks:
    idx, x, y, w, h, label, sub, ax1, ay1, ax2, ay2 = blk
    # 自适应高度
    if h is None:
      h = 70
    # 序号印
    draw_seq_badge(d, x, y, idx, size=48)
    # 面板
    draw_panel(d, x + 54, y - 2, w, h)
    # 文字
    try:
      ft = ImageFont.truetype(FONT_TITLE, 18)
      fs = ImageFont.truetype(FONT_SUB,   14)
    except Exception:
      ft = ImageFont.load_default()
      fs = ft
    tx = x + 64
    ty = y + 10
    d.text((tx, ty), label, font=ft, fill=COL_PAPER)
    ty2 = ty + 26
    d.text((tx, ty2), sub,  font=fs, fill=(180, 165, 130))
    # 箭头
    if ax1 is not None:
      draw_arrow(d, ax1, ay1, ax2, ay2, color=COL_GOLD, w=3)

  out = Image.alpha_composite(img, overlay)
  # 输出
  save_to = os.path.join(SHOTS, src.replace('.png', '.annotated.png'))
  out.convert('RGB').save(save_to, 'PNG', optimize=True)
  print('annotated:', save_to)
  return True

if __name__ == '__main__':
  n = 0
  for src, blocks in ANNOT:
    if annotate_one(src, blocks):
      n += 1
  print(f'\n共加注 {n} 张')
