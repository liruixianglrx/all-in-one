from parsimonious import NodeVisitor

# When making any change to `VerilogVisitor`,
# please run `parser_test.py` to make sure everything works fine.


class VerilogVisitor(NodeVisitor):
    def visit_Main(self, node, visited_children):
        """
        Main = Comment* ModuleDef Sentence ModuleEnd Comment*
        """

        _, module_info, sentence, *_ = visited_children
        module_name, io_dict = module_info
        sentence.update(io_dict)

        return sentence

    def visit_ModuleDef(self, node, visited_children):
        """
        ModuleDef = ModuleHead ModuleName Space Open PortList Close End
        """

        _, module_name, _, _, port_list, *_ = visited_children
        return module_name, {"IO": port_list}

    def visit_Sentence(self, node, visited_children):
        """Main body of code

        Sentence = (Def / Inst / Assign / Comment)*
        """
        sentence_output = {}

        for child in visited_children:
            child_key = list(child[0].keys())[0]
            # if sentence is a comment, skip it.
            if child_key == "comment":
                continue

            # The key already exists
            if child_key in sentence_output.keys():
                original_info = sentence_output[child_key]
                new_info = original_info + child[0][child_key]
                sentence_output[child_key] = new_info
            else:
                sentence_output.update(child[0])

        return sentence_output

    # ===== Definition related =====
    def visit_Def(self, node, visited_children):
        """
        Def = ~"input|output|wire" DefBase

        returns dict {str: set}
        """

        def_type, port_list = visited_children
        def_type = def_type.text

        return {def_type: port_list}

    def visit_DefBase(self, node, visited_children):
        """
        DefBase = WidthSel? PortList End
        """

        width, port_list, _ = visited_children
        # if input with a width, unfold it
        if isinstance(width, list):
            msb, lsb = width[0]
            unfold_port_list = []
            for port in port_list:
                for i in range(lsb, msb + 1):
                    unfold_port_list.append(port + "__" + str(i))
            return unfold_port_list
        # if input without width indicator
        else:
            return port_list

    # ===== Assign =====
    def visit_Assign(self, node, visited_children):
        """E.g. `assign out = in;`

        Assign = "assign" Port "=" Port End
        """

        _, port_1, _, port_2, _ = visited_children

        return {"assign": (port_1, port_2)}

    # ===== Gate Instantiation =====
    def visit_Inst(self, node, visited_children):
        """
        Inst = ~"NOT|BUF|AND|NAND|OR|NOR|XOR|XNOR"i InstBase
        """

        inst_type, inst_info = visited_children
        inst_type = inst_type.text.upper()

        return {inst_type: inst_info}

    def visit_InstBase(self, node, visited_children):
        """
        InstBase = Space InstName? Space Open (InstPorts / PortList) Close End
        """
        # dont care InstName
        _, _, _, _, port_list, _, _ = visited_children

        return port_list

    def visit_InstPorts(self, node, visited_children):
        """
        InstPorts = ("." Port "(" Port ")" ("," / "") Space)+
        """

        port_list = []
        for child in visited_children:
            port_list.insert(0, child[3])

        return port_list

    # ===== Port related =====
    def visit_PortList(self, node, visited_children):
        """E.g. `a, b, c`

        PortList = (Port ("," / ""))+
        """

        port_list = []
        for child in visited_children:
            port_list.append(child[0])

        return port_list

    def visit_Port(self, node, visited_children):
        """
        Support constant`1'b0`, selected port`a[0]`, port`clk`

        Port = Space (Constant / SelPort / Text) Space
        """

        _, port, _ = visited_children

        return port[0]

    def visit_SelPort(self, node, visited_children):
        """E.g. `port[n]`, change to `port__n`

        SelPort = Text "[" Number "]"
        """

        port_base, _, num, _ = visited_children
        new_port = port_base + "__" + num

        return new_port

    def visit_Constant(self, node, visited_children):
        """`1'b0` / `1'b1`, change to `0` / `1` respectively.

        Constant = "1'b" ~"\d"
        """

        _, num = visited_children

        return num.text

    # ===== Basic =====
    def visit_WidthSel(self, node, visited_children):
        """E.g. `[msb:lsb]`

        WidthSel = Space "[" Number ":" Number "]" Space
        """
        _, _, msb, _, lsb, *_ = visited_children

        return int(msb), int(lsb)

    def visit_Number(self, node, visited_children):
        """Basic Number visit method."""

        return node.text

    def visit_Text(self, node, visited_children):
        """Basic Text visit method."""

        return node.text

    def visit_Comment(self, node, visited_children):
        """Comment visit method."""

        return {"comment": None}

    def generic_visit(self, node, visited_children):
        """The generic visit method."""

        return visited_children or node
