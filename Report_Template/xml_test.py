from pathlib import Path
from typing import Optional

import xml.dom.minidom
from xml.dom.minidom import Element, Text, parse
import xml.etree.ElementTree as ET


XML_PATH = Path("Report_Template/Report_Template.xml")


def get_first_child_by_tag(node: Element, tag_name: str) -> Optional[Element]:
    if not isinstance(node, Element):
        return None
    elements = node.getElementsByTagName(tag_name)
    if not elements:
        return None
    first = elements[0]
    return first if isinstance(first, Element) else None

def get_cell_text(cell: Element) -> str:
    data_element = get_first_child_by_tag(cell, "Data")
    if data_element is None:
        return "None"
    text_node = next(
        (child for child in data_element.childNodes if isinstance(child, Text)),
        None,
    )
    return text_node.data if text_node is not None else "None"

def main() -> int:
    if not XML_PATH.exists() or not XML_PATH.is_file():
        print(f"XML 文件不存在: {XML_PATH}")
        return 1

    try:
        dom_tree = parse(XML_PATH.as_posix())
    except Exception as exc:  # noqa: BLE001
        print(f"解析 XML 失败: {exc}")
        return 1

    collection = dom_tree.documentElement
    if not isinstance(collection, Element):
        print("XML 根节点缺失或类型异常")
        return 1

    worksheets = collection.getElementsByTagName("Worksheet")
    if not worksheets:
        print("未找到 Worksheet 节点")
        return 1

    worksheet = worksheets[0]
    if not isinstance(worksheet, Element):
        print("Worksheet 节点类型异常")
        return 1

    table = get_first_child_by_tag(worksheet, "Table")
    if table is None:
        print("Worksheet 下未找到 Table 节点")
        return 1

    rows = table.getElementsByTagName("Row")
    if not rows:
        print("Table 下未找到 Row 节点")
        return 0

    for row in rows:
        if not isinstance(row, Element):
            continue
        print("***** New Row *****")
        cells = row.getElementsByTagName("Cell")
        if not cells:
            print("None")
            continue
        for cell in cells:
            if not isinstance(cell, Element):
                print("None")
                continue
            print(get_cell_text(cell))

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
