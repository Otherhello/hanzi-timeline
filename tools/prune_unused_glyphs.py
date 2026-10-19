"""删除 public/glyphs 下未被 characters.ts 引用的图，保持仓库精简。

用法：python tools/prune_unused_glyphs.py        # 仅列出
      python tools/prune_unused_glyphs.py --apply
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHARS = ROOT / "src" / "data" / "characters.ts"
GLYPHS = ROOT / "public" / "glyphs"


def main() -> int:
    text = CHARS.read_text(encoding="utf-8")
    used = {Path(m).name for m in re.findall(r"imageSrc:\s*'([^']+)'", text)}
    files = [p for p in GLYPHS.iterdir() if p.is_file()]
    unused = sorted(p for p in files if p.name not in used)

    print(f"引用 {len(used)} 张；目录 {len(files)} 个文件；未引用 {len(unused)} 个")
    for p in unused:
        print(f"  {p.name}  {p.stat().st_size}B")

    if "--apply" in sys.argv and unused:
        for p in unused:
            p.unlink()
        print(f"已删除 {len(unused)} 个未引用文件。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
