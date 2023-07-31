from parsimonious.grammar import Grammar

# After making any change to `verilog_grammar`,
# please run `parser_test.py` to make sure everything works fine.

verilog_grammar = Grammar(
    r"""
    # ----- Main -----
    Main       = Comment* ModuleDef Sentence ModuleEnd Comment*

    ModuleDef  = ModuleHead ModuleName Space Open PortList Close End
    Sentence   = (Def / Inst / Assign / Comment)*

    # ----- Definition -----
    Def        = ~"input|output|wire" DefBase
    DefBase    = WidthSel? PortList End

    # ----- Assign -----
    Assign     = "assign" Port "=" Port End

    # ----- Logic Gate Instantiation -----
    Inst       = ~"NOT|BUF|AND|NAND|OR|NOR|XOR|XNOR"i InstBase
    InstBase   = Space InstName? Space Open (InstPorts / PortList) Close End

    # ----- Basic -----
    ModuleHead = "module" Space
    ModuleEnd  = "endmodule" Space

    ModuleName = Text
    InstPorts  = ("." Port "(" Port ")" ("," / "") Space)+
    PortList   = (Port ("," / ""))+
    Port       = Space (Constant / SelPort / Text) Space
    SelPort    = Text "[" Number "]"  # port[n]
    Constant   = "1'b" ~"\d"          # 1'b0 / 1'b1
    InstName   = Text
    WidthSel   = Space "[" Number ":" Number "]" Space

    Text       = ~"\w+"
    Comment    = Space (LineCmt / BlockCmt) Space
    LineCmt    = ~"\n"* "//" (!~"\n" ~".")* ~"\n"
    BlockCmt   = ~"\/\*[\s\S]*\*\/"
    Open       = "(" Space
    Close      = ")" Space
    End        = ";" Space

    Number     = ~"\d+"
    Space      = ~"\s*"
    """
)
