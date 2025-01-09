section .data
    a db "Systems -2",10,0
    b db "Assembler"
    c dw 5
    d dw 10,20,30
    e dd 5
    f dd 10,20,30
    g dq 5
    h dq 10,20,30

section .bss
    i resb 10
    j resw 10
    k resd 10
    l resq 10

section .text
    global main

main:

add_in:
    add eax, eax
    add eax, ebx
    add eax, ecx
    add eax, edx
    add ebx, eax
    add ebx, ebx
    add ebx, ecx
    add ebx, edx
    add ecx, eax
    add ecx, ebx
    add ecx, ecx
    add ecx, edx
    add edx, eax
    add edx, ebx
    add edx, ecx
    add edx, edx
    add eax, 555
    add eax, [ebx]
    add ebx, [eax]
    add eax,[ebx+555]
    add edx,[ecx+555]
    add [ebx+555],ecx
    add ebx, [g+555]
    add [g+555],eax
    add [ebx], ecx

sub_in:
    sub eax, eax
    sub eax, ebx
    sub eax, ecx
    sub eax, edx
    sub ebx, eax
    sub ebx, ebx
    sub ebx, ecx
    sub ebx, edx
    sub ecx, eax
    sub ecx, ebx
    sub ecx, ecx
    sub ecx, edx
    sub edx, eax
    sub edx, ebx
    sub edx, ecx
    sub edx, edx
    sub eax, 555
    sub eax, [ebx]
    sub ebx, [eax]
    sub eax,[ebx+555]
    sub edx,[ecx+555]
    sub [ebx+555],ecx
    sub ebx, [g+555]
    sub [g+555],eax
    sub [ebx], ecx
    

cmp_in:
    cmp eax, eax
    cmp eax, ebx
    cmp eax, ecx
    cmp eax, edx
    cmp ebx, eax
    cmp ebx, ebx
    cmp ebx, ecx
    cmp ebx, edx
    cmp ecx, eax
    cmp ecx, ebx
    cmp ecx, ecx
    cmp ecx, edx
    cmp edx, eax
    cmp edx, ebx
    cmp edx, ecx
    cmp edx, edx
    cmp eax, 555
    cmp eax, [ebx]
    cmp ebx, [eax]
    cmp eax,[ebx+555]
    cmp edx,[ecx+555]
    cmp ebx, [g+555]
    cmp [g+555],eax
    cmp [ebx], ecx

jmp_in:
    jmp 555
    jmp eax
    jmp ecx
    jmp edx
    jmp eax
    jmp [eax]
    jmp [ecx]
    jmp [edx]
    jmp [ebx]   
    jmp [e]
    jmp [eax+555]
    jmp [ecx+555]
    jmp [edx+555]
    jmp [ebx+555]
    jmp [e+555]

inc_in:
    inc eax
    inc ecx
    inc edx
    inc ebx
    ;inc e
    ;inc dword[eax]
    ;inc dword[ecx]
    ;inc dword[edx]
    ;inc dword[ebx]
    ;inc dword[a]
    ;inc dword[eax+555]
    ;inc dword[ecx+555]
    ;inc dword[edx+555]
    ;inc dword[ebx+555]
    ;inc dword[e+555]

dec_in:
    dec ecx
    dec edx
    dec ebx
    ;dec e
    ;dec dword[eax]
    ;dec dword[ecx]
    ;dec dword[edx]
    ;dec dword[ebx]
    ;dec dword[a]
    ;dec dword[eax+555]
    ;dec dword[ecx+555]
    ;dec dword[edx+555]
    ;dec dword[ebx+555]
    ;dec dword[e+555]

xor_in:
    xor eax, eax
    xor eax, ebx
    xor eax, ecx
    xor eax, edx
    xor ebx, eax
    xor ebx, ebx
    xor ebx, ecx
    xor ebx, edx
    xor ecx, eax
    xor ecx, ebx
    xor ecx, ecx
    xor ecx, edx
    xor edx, eax
    xor edx, ebx
    xor edx, ecx
    xor edx, edx
    xor eax, 555
    xor eax, [ebx]
    xor ebx, [eax]
    xor eax,[ebx+555]
    xor edx,[ecx+555]
    xor [ebx+555],ecx
    xor ebx, [g+555]
    xor [g+555],eax
    xor [ebx], ecx



mul_in:
    mul eax
    mul ebx
    mul ecx
    mul edx
    ;mul e
    ;mul dword[eax]
    ;mul dword[eax+555]
    ;mul ebx
    ;mul dword[ebx]
    ;mul dword[ebx+555]

div_in:
    div eax
    div ecx
    div edx
    div ebx
    ;div e
    ;div dword[eax]
    ;div dword[eax+555]
    ;div ebx
    ;div dword[ebx]
    ;div dword[ebx+555]

jz_in:
    jz 555

jnz_in:
    jnz 555
