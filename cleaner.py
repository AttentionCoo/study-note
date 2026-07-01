"""
项目清理脚本：删除多余文件
1. 删除 assets/images/ 中未被任何 .md 文件引用的孤立图片
2. 报告 .md 文件中引用了外部路径的失效图片链接
3. 删除 .md 文件中指向外部路径的失效图片行
"""

import os
import re
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets", "images")


def find_all_md_files(root):
    md_files = []
    for dirpath, _, filenames in os.walk(root):
        if ".git" in dirpath:
            continue
        for f in filenames:
            if f.endswith(".md"):
                md_files.append(os.path.join(dirpath, f))
    return md_files


def find_all_images(assets_dir):
    images = set()
    if not os.path.isdir(assets_dir):
        return images
    for f in os.listdir(assets_dir):
        if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp")):
            images.add(f)
    return images


def extract_image_references(md_files):
    referenced_local = set()
    broken_refs = []
    pattern = re.compile(r"!\[.*?\]\((.*?)\)")
    for md_path in md_files:
        with open(md_path, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                for match in pattern.finditer(line):
                    ref = match.group(1)
                    if ref.startswith(("http://", "https://")):
                        continue
                    filename = os.path.basename(ref)
                    if filename:
                        referenced_local.add(filename)
                    if ref.startswith(("C:", "D:", "../AppData", "AppData")):
                        broken_refs.append((md_path, line_num, ref.strip()))
    return referenced_local, broken_refs


def delete_orphaned_images(assets_dir, all_images, referenced_images, auto=False):
    orphaned = all_images - referenced_images
    if not orphaned:
        print("\n✅ 没有孤立图片需要删除。")
        return []

    print(f"\n🗑️  发现 {len(orphaned)} 个孤立图片（未被任何 .md 引用）：")
    deleted = []
    for img in sorted(orphaned):
        path = os.path.join(assets_dir, img)
        size_kb = os.path.getsize(path) / 1024
        print(f"   - {img}  ({size_kb:.1f} KB)")
        deleted.append(path)

    total_size = sum(os.path.getsize(p) for p in deleted) / (1024 * 1024)
    print(f"\n   合计可释放空间: {total_size:.1f} MB")

    if auto:
        confirm = "y"
    else:
        confirm = input("\n⚠️  确认删除以上孤立图片？(y/N): ").strip().lower()
    if confirm == "y":
        for path in deleted:
            os.remove(path)
        print(f"✅ 已删除 {len(deleted)} 个孤立图片。")
    else:
        print("❌ 已取消删除。")
        deleted = []

    return deleted


def clean_broken_refs(md_files, broken_refs, auto=False):
    if not broken_refs:
        print("\n✅ 没有失效的图片引用。")
        return

    print(f"\n🔗 发现 {len(broken_refs)} 处失效图片引用（指向本地外部路径）：")
    by_file = {}
    for md_path, line_num, ref in broken_refs:
        rel = os.path.relpath(md_path, PROJECT_ROOT)
        print(f"   - {rel}:{line_num}  → {ref}")
        by_file.setdefault(md_path, []).append(line_num)

    if auto:
        confirm = "y"
    else:
        confirm = input("\n⚠️  确认从 .md 文件中删除这些失效图片行？(y/N): ").strip().lower()
    if confirm != "y":
        print("❌ 已取消。")
        return

    for md_path, line_nums in by_file.items():
        with open(md_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        new_lines = [l for i, l in enumerate(lines, 1) if i not in set(line_nums)]
        with open(md_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
    print(f"✅ 已从 {len(by_file)} 个文件中清理失效引用。")


def main():
    auto = "--auto" in sys.argv

    print("=" * 60)
    print("📂 项目清理工具")
    if auto:
        print("   ⚡ 自动模式（无需确认）")
    print(f"   项目根目录: {PROJECT_ROOT}")
    print(f"   图片目录:   {ASSETS_DIR}")
    print("=" * 60)

    md_files = find_all_md_files(PROJECT_ROOT)
    all_images = find_all_images(ASSETS_DIR)
    print(f"\n📄 扫描到 {len(md_files)} 个 Markdown 文件")
    print(f"🖼️  扫描到 {len(all_images)} 个图片文件")

    referenced_images, broken_refs = extract_image_references(md_files)
    print(f"🔗 其中有 {len(referenced_images)} 个被 .md 文件引用")
    print(f"❌ 其中有 {len(broken_refs)} 处指向外部路径的失效引用")

    delete_orphaned_images(ASSETS_DIR, all_images, referenced_images, auto=auto)
    clean_broken_refs(md_files, broken_refs, auto=auto)

    print("\n" + "=" * 60)
    print("🎉 清理完成！")


if __name__ == "__main__":
    main()