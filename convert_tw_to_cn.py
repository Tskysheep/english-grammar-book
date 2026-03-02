"""
根据 Terminology.md 术语表，将 Ver3 目录下 md 文档中的台湾术语替换为大陆术语。

替换顺序：长词优先，避免短词先替换导致长词被破坏。
例如 "介系词片语" 必须在 "介系词" 之前替换。
"""

import os
import glob

# 台湾 -> 大陆 术语映射（从 Terminology.md 提取）
TERM_MAP = {
    # ---- 复合词（长词优先） ----
    '对等连接词': '并列连词',
    '所有格代名词': '物主代词',
    '介系词片语': '介词短语',
    '名词片语': '名词短语',
    '动词片语': '动词短语',
    '主词子句': '主语从句',
    '受词子句': '宾语从句',
    '形容词子句': '表语从句',
    '副词子句': '状语从句',
    '连缀动词': '系动词',
    '行动动词': '行为动词',
    '个别动词': '单个动词',
    '简单现在式': '一般现在时',
    '简单未来式': '一般将来时',
    '过去未来式': '过去将来时',
    '现在进行式': '现在进行时',
    '过去进行式': '过去进行时',
    '现在完成式': '现在完成时',
    '过去完成式': '过去完成时',
    '是否疑问句': '一般疑问句',
    '讯息疑问句': '特殊疑问句',
    '无声子音': '清辅音',
    '有声子音': '浊辅音',
    # ---- 基础词（短词后替换） ----
    '代名词': '代词',
    '连接词': '连词',
    '介系词': '介词',
    '片语': '短语',
    '主词': '主语',
    '受词': '宾语',
    '子句': '从句',
    '受格': '宾格',
    '文法': '语法',
    '单字': '单词',
    '简单式': '一般时',
    '进行式': '进行时',
    '完成式': '完成时',
    '不定词': '不定式',
    '母音': '元音',
    '子音': '辅音',
}

# 按词长降序排列，确保长词先替换
SORTED_TERMS = sorted(TERM_MAP.keys(), key=len, reverse=True)


def process_file(filepath):
    """处理单个文件，返回替换次数"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    total = 0

    for tw_term in SORTED_TERMS:
        cn_term = TERM_MAP[tw_term]
        count = content.count(tw_term)
        if count > 0:
            content = content.replace(tw_term, cn_term)
            total += count

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    return total


def main():
    content_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'docs', 'content', 'Ver3'
    )

    md_files = sorted(glob.glob(os.path.join(content_dir, '*.md')))
    total_changes = 0

    for filepath in md_files:
        filename = os.path.basename(filepath)
        # 跳过术语表本身
        if filename == 'Terminology.md':
            continue
        changes = process_file(filepath)
        if changes > 0:
            print(f'  {filename}: {changes} replacements')
            total_changes += changes

    print(f'\nTotal: {total_changes} replacements across {len(md_files) - 1} files')


if __name__ == '__main__':
    main()
