class SymbolEntry:
    def __init__(self, Symbol_Name, Type, Size, Value=None, Scope=None, Address=None):
        self.Symbol_Name = Symbol_Name
        self.Type = Type
        self.Size = Size
        self.Value = Value
        self.Scope = Scope
        self.Address = Address

    def __repr__(self):
        return (f"Symbol_Name={self.Symbol_Name}, "
                f"Type={self.Type}, Size={self.Size}, Value={self.Value}, "
                f"Scope={self.Scope}, Address={self.Address})")


class LiteralEntry:
    def __init__(self, SrNo, Literal, Type, Size, Value=None, Scope=None, Address=None):
        self.SrNo = SrNo
        self.Literal = Literal
        self.Type = Type
        self.Size = Size
        self.Value = Value
        self.Scope = Scope
        self.Address = Address

    def __repr__(self):
        return (f"LiteralEntry(SrNo={self.SrNo}, Literal={self.Literal}, "
                f"Type={self.Type}, Size={self.Size}, Value={self.Value}, "
                f"Scope={self.Scope}, Address={self.Address})")


class IntermediateCodeEntry:
    def __init__(self, Line_Number, Size, Opcode, Instruction, Address):
        self.Line_Number = Line_Number
        self.Size = Size
        self.Opcode = Opcode
        self.Instruction = Instruction
        self.Address = Address

    def __repr__(self):
        return (f"IntermediateCodeEntry(Line_Number={self.Line_Number}, "
                f"Size={self.Size}, Opcode={self.Opcode}, Instruction={self.Instruction},Address={self.Address})")

class OpcodeInstruction:
    def __init__(self, opcode, instruction, num_params, param1, param2, size, is_modr, rd):
        self.opcode = opcode
        self.instruction = instruction
        self.num_params = num_params
        self.param1 = param1
        self.param2 = param2
        self.size = size
        self.is_modr = is_modr
        self.rd = rd

    def __repr__(self):
        return (f"OpcodeInstruction(opcode={self.opcode}, instruction={self.instruction}, "
                f"num_params={self.num_params}, param1={self.param1}, param2={self.param2}, "
                f"size={self.size}, is_modr={self.is_modr}, rd={self.rd})")

class ErrorEntry:
    def __init__(self, Error_no, Error_Message, Address):
        self.Error_no = Error_no
        self.Error_Message = Error_Message
        self.Address = Address
    def __repr__(self):
        return (f"ErrorEntry(Error_no={self.Error_no}, "
                f"Error_Message={self.Error_Message}, Address={self.Address})")