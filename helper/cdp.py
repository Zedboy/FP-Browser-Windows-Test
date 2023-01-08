import math
import time


def get_node_id(element):
    """
    获得 nodeID
    """
    if isinstance(element, (dict)):
        if "root" in element:
            node_id = element.get('root').get('nodeId')
        else:
            node_id = element.get('nodeId')
    else:
        node_id = element

    return node_id


def compute_position(element, driver):
    """
    计算点击的位置
    """
    btn_quads = None
    i = 0
    max = 3
    while True:
        i += 1
        if i > max:
            break

        try:
            btn_quads = driver.execute_cdp_cmd("DOM.getContentQuads", {
                "nodeId": get_node_id(element=element),
            })

            if btn_quads and "quads" in btn_quads:
                break
        except:
            pass

        # 如果没有找到，则 sleep 1秒
        time.sleep(1)

    if btn_quads is None:
        raise Exception("元素坐标没有找到")

    btn_quads = btn_quads.get('quads')[0]
    # [1105.666748046875, 265.97918701171875, 1457.666748046875, 265.97918701171875, 1457.666748046875, 297.97918701171875, 1105.666748046875, 297.97918701171875]

    width = btn_quads[2] - btn_quads[0]
    height = btn_quads[7] - btn_quads[1]

    # print(btn_quads)
    # print(width, height)

    # 计算点击的位置
    offset_width = math.ceil(width / 2)
    offset_height = math.ceil(height / 2)

    return btn_quads[0] + offset_width, btn_quads[1] + offset_height


def click_ele(ele, driver):
    """
    点击元素
    """
    # 计算点击的位置
    x, y = compute_position(element=ele, driver=driver)

    # 按下按钮
    driver.execute_cdp_cmd("Input.dispatchMouseEvent", {
        "type": "mousePressed",
        "x": x,
        "y": y,
        "button": "left",
        "clickCount": 1,
    })

    driver.execute_cdp_cmd("Input.dispatchMouseEvent", {
        "type": "mouseReleased",
        "x": x,
        "y": y,
        "button": "left",
        "clickCount": 1,
    })


def loop_find_element(driver, selector, node_id, timeout=10):
    """
    循环查找元素
    """
    now = time.time()
    element = None

    while True:
        if math.ceil(time.time() - now) > timeout:
            break

        try:
            element = driver.execute_cdp_cmd("DOM.querySelector", {
                "nodeId": get_node_id(node_id),
                "selector": selector,
            })

            if check_element_exists(ele=element):
                return element
        except:
            pass

        time.sleep(1)

    if check_element_exists(element):
        return element

    return None


def check_element_exists(ele):
    """
    检测元素是否存在
    """
    return ele and "nodeId" in ele and ele.get('nodeId') > 0
