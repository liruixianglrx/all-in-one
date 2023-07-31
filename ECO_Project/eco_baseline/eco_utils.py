from eco_baseline.logic_tree.node import Node


def port_name_2_index(port_list: list[str], node_list: list[Node]) -> list[int]:
    index_list = []
    for port in port_list:
        for node_i in range(len(node_list)):
            if node_list[node_i].node_name == port:
                index_list.append(node_i)
                break
    return index_list


def nodes_2_values(node_list: list[Node]) -> list[int]:
    return [node.value for node in node_list]


SINGAL_TARGET = [1, 2, 3, 4, 7, 8, 12, 13, 15, 18]
