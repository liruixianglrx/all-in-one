import json
import numpy as np
from eco_baseline.logic_tree.node import Node
import  eco_baseline.logic_tree.gate as gt
# from eco_baseline.logic_tree.gate import Gate
class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Node):
            return {
                "__type__" :"Node",
                "node_name":obj.node_name,
                "level": obj.level,
                "value" :obj.value,
                "driver_index" : obj.driver_index,
                "load_index":obj.load_index
            }

        if isinstance(obj, gt.Gate):
            return {
                "__type__" :"Gate",
                "gate_type":"Not" if isinstance(obj,gt.Not) else
                            "Buf" if isinstance(obj,gt.Buf) else
                            "And" if isinstance(obj,gt.And) else
                            "Nand" if isinstance(obj, gt.Nand) else
                            "Or" if isinstance(obj, gt.Or) else
                            "Nor" if isinstance(obj, gt.Nor) else
                            "Xor" if isinstance(obj, gt.Xor) else
                            "Xnor" if isinstance(obj, gt.Xnor) else "None",
                "input_index" : obj.input_index,
                "output_index" : obj.output_index
            }

        return super().default(obj)
