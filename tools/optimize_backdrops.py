"""
纸背图优化：JPEG → WebP，并把模糊直接「烤」进像素。

为什么这么做：
1. 纸背最终要盖一层 blur(9px)。浏览器对整屏固定元素做高斯模糊，
   每一帧都要重算，滚动时尤其明显；而模糊后的图片压缩率极高，
   烘焙后 1400px 宽只有约 14KB（原 JPEG 100–290KB）。
2. 只加载一幅/次，所以单文件体积直接等于首屏代价。

模糊半径按「最终按 1400 CSS px 宽显示」换算，避免大图糊过头、小图不够糊。
"""
import os
import sys

from PIL import Image, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(ROOT, 'public', 'backdrops')

REF_WIDTH = 1400      # 参照显示宽度（CSS px）
REF_BLUR = 9          # 与 index.css 里原先的 blur(9px) 对应
MAX_EDGE = 1400       # 输出最长边
QUALITY = 70


def main(apply: bool):
    files = sorted(f for f in os.listdir(DIR) if f.lower().endswith('.jpg'))
    if not files:
        print('没有待处理的 jpg')
        return
    total_old = total_new = 0
    for fn in files:
        src = os.path.join(DIR, fn)
        im = Image.open(src).convert('RGB')
        w, h = im.size
        scale = MAX_EDGE / max(w, h)
        if scale < 1:
            w2, h2 = max(1, round(w * scale)), max(1, round(h * scale))
            im = im.resize((w2, h2), Image.LANCZOS)
        else:
            w2, h2 = w, h
        radius = max(1.5, REF_BLUR * w2 / REF_WIDTH)
        im = im.filter(ImageFilter.GaussianBlur(radius))

        out = src[:-4] + '.webp'
        im.save(out, 'WEBP', quality=QUALITY, method=6)
        old_kb = os.path.getsize(src) / 1024
        new_kb = os.path.getsize(out) / 1024
        total_old += old_kb
        total_new += new_kb
        print(f'{fn:22s} {old_kb:7.1f}KB -> {os.path.basename(out):22s} '
              f'{new_kb:6.1f}KB  ({w2}x{h2}, r={radius:.1f})')
        if apply:
            os.remove(src)
    print(f'\n合计 {total_old:.1f}KB -> {total_new:.1f}KB '
          f'(省 {100 * (1 - total_new / total_old):.0f}%)  单幅均 {total_new / len(files):.1f}KB')
    if not apply:
        print('（预览模式，未删除 jpg；加 --apply 落实）')


if __name__ == '__main__':
    main('--apply' in sys.argv)
