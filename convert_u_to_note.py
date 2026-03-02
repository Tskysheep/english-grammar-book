"""
将 EnglishGrammarBook 中 <u>...</u> + 标注行 的模式
转换为 <Note note="X">...</Note> 的 VuePress 组件语法。

转换示例：
  输入：
    <u>The dog</u> <u>barked</u> at the mailman.
    S V
  输出：
    <Note note="S">The dog</Note> <Note note="V">barked</Note> at the mailman.

规则：
  1. 上一行有 <u>...</u> 标签，下一行是 S/V/O/C 等标注
  2. 根据每个 <u> 在上一行中的字符位置，匹配下一行同一位置的标注词
  3. 将 <u>X</u> 替换为 <Note note="标注">X</Note>
  4. 删除标注行
  5. 不含 <u> 的行或标注行不匹配的行保持不变
"""

import re
import os
import glob


# 标注行的正则：以 S 开头，包含 V，后面是标注字符和可能的中文说明
ANNOTATION_RE = re.compile(
    r'^S\s+V'   # 以 S 空格 V 开头
)

# 有效的标注 token（只把这些映射为 Note）
VALID_LABELS = {'S', 'V', 'O', 'C', 'O1', 'O2'}


def has_u_tags(line):
    """检查行中是否包含 <u>...</u> 标签"""
    return '<u>' in line and '</u>' in line


def is_annotation_line(line):
    """检查是否为 S V O C 标注行"""
    stripped = line.strip()
    if not stripped:
        return False
    return ANNOTATION_RE.match(stripped) is not None


def parse_u_positions(line):
    """
    解析一行中所有 <u>...</u> 的起止位置（按渲染后的字符位置）。
    返回 [(render_start, render_end, content), ...]
    """
    results = []
    render_pos = 0
    i = 0
    raw = line

    while i < len(raw):
        if raw[i:].startswith('<u>'):
            # 找到 <u> 标签
            start_render = render_pos
            i += 3  # 跳过 <u>
            # 找 </u>
            end_tag = raw.find('</u>', i)
            if end_tag == -1:
                break
            content = raw[i:end_tag]
            # 计算内容的渲染长度
            render_end = start_render + len(content)
            results.append((start_render, render_end, content))
            render_pos = render_end
            i = end_tag + 4  # 跳过 </u>
        else:
            render_pos += 1
            i += 1

    return results


def parse_annotation_tokens(line):
    """
    解析标注行，返回 [(start_pos, end_pos, token), ...]
    token 为 S/V/O/C/(adv.) 等
    """
    tokens = []
    stripped = line.rstrip('\n')
    i = 0
    while i < len(stripped):
        if stripped[i] == ' ':
            i += 1
            continue

        # 尝试匹配多字符 token
        start = i

        # 跳过半角/全角括号及其内容
        if stripped[i] in '(（':
            close = ')' if stripped[i] == '(' else '）'
            end = stripped.find(close, i)
            i = (end + 1) if end != -1 else len(stripped)
            continue

        # 匹配 O1, O2 等
        if i + 1 < len(stripped) and stripped[i] in 'SVOC' and stripped[i + 1:i + 2].isdigit():
            token = stripped[i:i + 2]
            i += 2
        # 匹配单字符 S/V/O/C
        elif stripped[i] in 'SVOC':
            token = stripped[i]
            i += 1
        else:
            # 非标注字符，跳到行尾（后面的是中文说明等）
            break

        tokens.append((start, i, token))

    return tokens


def match_labels_to_u_tags(u_positions, annotation_tokens):
    """
    将标注 token 匹配到对应的 <u> 标签。
    匹配策略：按顺序一一对应。
    返回 {u_index: label}
    """
    mapping = {}

    if len(annotation_tokens) == 0 or len(u_positions) == 0:
        return mapping

    # 策略 1：数量相同时直接按顺序一一对应
    if len(annotation_tokens) == len(u_positions):
        for idx, (_, _, token) in enumerate(annotation_tokens):
            if token in VALID_LABELS:
                mapping[idx] = token
        return mapping

    # 策略 2：标注比 <u> 少，按位置最近匹配
    for ann_start, ann_end, token in annotation_tokens:
        if token not in VALID_LABELS:
            continue
        ann_center = (ann_start + ann_end) / 2.0

        best_idx = None
        best_dist = float('inf')
        for idx, (u_start, u_end, _) in enumerate(u_positions):
            if idx in mapping:
                continue
            u_center = (u_start + u_end) / 2.0
            dist = abs(ann_center - u_center)
            if dist < best_dist:
                best_dist = dist
                best_idx = idx

        if best_idx is not None:
            mapping[best_idx] = token

    return mapping


def replace_u_with_notes(line, mapping, u_positions):
    """
    将行中的 <u>...</u> 替换为 <Note note="X">...</Note>。
    mapping: {u_index: label}
    """
    result = []
    u_index = 0
    i = 0
    raw = line

    while i < len(raw):
        if raw[i:].startswith('<u>'):
            end_tag = raw.find('</u>', i + 3)
            if end_tag == -1:
                result.append(raw[i:])
                break
            content = raw[i + 3:end_tag]

            if u_index in mapping:
                label = mapping[u_index]
                result.append(f'<Note note="{label}">{content}</Note>')
            else:
                # 保留原始 <u> 标签
                result.append(f'<u>{content}</u>')

            u_index += 1
            i = end_tag + 4
        else:
            result.append(raw[i])
            i += 1

    return ''.join(result)


def extract_trailing_text(line):
    """
    从标注行中提取尾部的中文翻译文本。
    例如 'S V O C （我看到树在风中摇摆。）' -> '（我看到树在风中摇摆。）'
    例如 'S V O (任何人都可以赢得一千元。)' -> '(任何人都可以赢得一千元。)'
    """
    stripped = line.strip()
    i = 0
    while i < len(stripped):
        if stripped[i] == ' ':
            i += 1
            continue
        if stripped[i] in 'SVOC' and (i + 1 >= len(stripped) or stripped[i + 1] in ' SVOC(（' or stripped[i + 1].isdigit()):
            if i + 1 < len(stripped) and stripped[i + 1].isdigit():
                i += 2
            else:
                i += 1
            continue
        # 跳过空格后的非 SVOC 内容即为尾部文本
        break
    trailing = stripped[i:].strip()
    return trailing if trailing else None


def process_file(filepath):
    """处理单个 Markdown 文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    i = 0
    changes = 0

    while i < len(lines):
        current_line = lines[i]

        # 检查当前行是否有 <u> 标签，且下一行是标注行
        if has_u_tags(current_line) and i + 1 < len(lines) and is_annotation_line(lines[i + 1]):
            u_positions = parse_u_positions(current_line)
            annotation_tokens = parse_annotation_tokens(lines[i + 1])
            mapping = match_labels_to_u_tags(u_positions, annotation_tokens)

            if mapping:
                new_line = replace_u_with_notes(current_line, mapping, u_positions)
                # 检查标注行是否有尾部翻译文本需要保留
                trailing = extract_trailing_text(lines[i + 1])
                new_lines.append(new_line)
                if trailing:
                    new_lines.append(trailing + '\n')
                # 跳过标注行
                i += 2
                changes += 1
                continue

        new_lines.append(current_line)
        i += 1

    if changes > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

    return changes


def main():
    content_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'docs', 'content'
    )

    md_files = sorted(glob.glob(os.path.join(content_dir, '*.md')))
    total_changes = 0

    for filepath in md_files:
        filename = os.path.basename(filepath)
        changes = process_file(filepath)
        if changes > 0:
            print(f'  {filename}: {changes} conversions')
            total_changes += changes

    print(f'\nTotal: {total_changes} conversions across {len(md_files)} files')


if __name__ == '__main__':
    main()
