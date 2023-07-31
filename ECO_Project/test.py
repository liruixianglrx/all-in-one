import yappi

from eco_baseline.eco import EcoEngine
from utils.utils import *

if __name__ == "__main__":
    # origin = "./dataset/new/unit7/F.v"
    # golden = "./dataset/new/unit7/G.v"
    origin = "./dataset/ICCAD2017/unit1/F.v"
    golden = "./dataset/ICCAD2017/unit1/G.v"

    engine = EcoEngine(origin, golden, early_stop=5)
    # print(engine.origin.masked_nodes)
    # yappi.set_clock_type("cpu")  # Use set_clock_type("wall") for wall time
    # yappi.start()

    engine.run_eco(
        searching_node_range=[2],
        comb_max=200,
        stratified=True,
        levels_per_layer=3,
        max_try=5,
        max_subtry=3,
        max_subsubtry=3,
    )

    print(engine.iter)

# yappi.get_func_stats().print_all()

# engine._run_traverse()
# engine.find_candidate_base(2)
# engine.print_possible_candidate()
# print(engine.miter.verify(engine.candidate_basenodes[0], silent=True))
# engine.generate_patch(engine.candidate_basenodes[0])
