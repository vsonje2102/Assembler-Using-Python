register_encoding = {
    "eax": 0b000,
    "ecx": 0b001,
    "edx": 0b010,
    "ebx": 0b011,
    "esp": 0b100,
    "ebp": 0b101,
    "esi": 0b110,
    "edi": 0b111,
}

inc_opcodes = {
    "eax": 0x40,
    "ecx": 0x41,
    "edx": 0x42,
    "ebx": 0x43,
    "esp": 0x44,
    "ebp": 0x45,
    "esi": 0x46,
    "edi": 0x47,
}
dec_opcodes = {
    "eax": 0x48,
    "ecx": 0x49,
    "edx": 0x4A,
    "ebx": 0x4B,
    "esp": 0x4C,
    "ebp": 0x4D,
    "esi": 0x4E,
    "edi": 0x4F,
}
mul_modrm = {
    "eax": 0xE0,
    "ecx": 0xE1,
    "edx": 0xE2,
    "ebx": 0xE3,
    "esp": 0xE4,
    "ebp": 0xE5,
    "esi": 0xE6,
    "edi": 0xE7,
}

div_modrm = {
    "eax": 0xF0,
    "ecx": 0xF1,
    "edx": 0xF2,
    "ebx": 0xF3,
    "esp": 0xF4,
    "ebp": 0xF5,
    "esi": 0xF6,
    "edi": 0xF7,
}
