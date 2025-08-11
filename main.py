import re
import massive_memory
import os

INST_CODES = {
    'nop':  0x00,
    'ldi':  0x01,
    'mov':  0x02,
    'add':  0x03,
    'sub':  0x04,
    'mul':  0x05,
    'div':  0x06,
    'and':  0x07,
    'not':  0x08,
    'or':   0x09,
    'xor':  0x0a,
    'shl':  0x0b,
    'shr':  0x0c,
    'cmp':  0x0d,
    'jmp':  0x0e,
    'jg':   0x0f,
    'je':   0x10,
    'jl':   0x11,
    'jng':  0x12,
    'jne':  0x13,
    'jnl':  0x14,
    'jz':   0x15,
    'jc':   0x16,
    'jnz':  0x17,
    'jnc':  0x18,
    'addi': 0x19,
    'subi': 0x1a,
    'muli': 0x1b,
    'divi': 0x1c,
    'wtb':  0x1d,
    'btw':  0x1e,
    'dwtw': 0x2f,
    'hlt':  0x20,
    'cmpi': 0x21,
    'ldm':  0x22,
    'ldmi': 0x23,
    'stm':  0x24,
    'stmi': 0x25,
}

REGISTER_CODES = {
    'r0':   0x0,
    'r1':   0x1,
    'r2':   0x2,
    'r3':   0x3,
    'r4':   0x4,
    'r5':   0x5,
    'r6':   0x6,
    'r7':   0x7,
    'r8':   0x8,
    'r9':   0x9,
    'ra':   0xa,
    'rb':   0xb,
    'rc':   0xc,
    'rd':   0xd,
    're':   0xe,
    'rf':   0xf,
    'ler0': 0x10,
    'uer0': 0x11,
    'ler1': 0x12,
    'uer1': 0x13,
    'ler2': 0x14,
    'uer2': 0x16,
    'ler3': 0x17,
    'uer3': 0x18,
    'ler4': 0x19,
    'uer4': 0x1a,
    'ler5': 0x1b,
    'uer5': 0x1c,
    'ler6': 0x1d,
    'uer6': 0x1e,
    'ler7': 0x1f,
    'uer7': 0x20,
}

with open("prog.asm", "rt") as f:
  program = f.read().split("\n")

def hex_check(s: str):
    pattern = r'^0[xX][0-9a-fA-F]'
    return bool(re.match(pattern, s))

def assemble_to_list(code: str):
  cm2_code_label_storage = {}
  instruction_lists = []
  for i, v in enumerate(code):
    instruction = v.split(" ")
    for idx, pt in enumerate(instruction):
      if re.match(r'^[a-zA-Z]+.*:$', pt):
        cm2_code_label_storage[pt.strip(":")] = i
        instruction = []
      
      if pt in cm2_code_label_storage:
        instruction[idx] = cm2_code_label_storage[pt]

      if re.match(r'^0[xX][0-9a-fA-F]', pt):
        instruction[idx] = int(pt, base=16)

      if pt in INST_CODES:
        instruction[idx] = INST_CODES[pt]

      if pt in REGISTER_CODES:
        instruction[idx] = REGISTER_CODES[pt]

    if instruction == []:
      continue
    
    instruction_lists.append(instruction)

    print(f"I: {instruction}")
  print(f"CM2 LABEL: {cm2_code_label_storage} \n")
  return instruction_lists

def write_file(fp_normal: str, lists: list, fp_cm2:str = 'None'):
  lines = [ [], [ [], [], [], [] ] ]
  for list_ in lists:
    current_line = ""
    for i, part in enumerate(list_):
      if not type(part) == str:
        if i == 0:
          current_line = f'{current_line}{part:02x}'
        else:
          current_line = f'{current_line}{part:04x}'
    

    current_line = current_line.ljust(14, '0')

    code, a, b, c = current_line[0:2], current_line[2:6], current_line[6:10], current_line[10:14]

    lines[0].append(current_line)
    lines[1][0].append(a)
    lines[1][1].append(b)
    lines[1][2].append(c)
    lines[1][3].append(code)
  
  with open(fp_normal, 'wt') as file:
    file.write('00000000000000\n' + '\n'.join(lines[0]))

  if fp_cm2 != 'None':
    for v in os.listdir(fp_cm2):
      if v == 'a':
        with open(f'{fp_cm2}/a', 'wt') as a_f:
          a_string = ''
          for v1 in lines[1][0]:
            a_string = f'{a_string}{massive_memory.integer_to_massive_memory(int(v1, base=16))}'
          a_string = a_string.ljust(12288, "A")
          a_f.write(f"AAA{a_string}")

      if v == 'b':
        with open(f'{fp_cm2}/b', 'wt') as b_f:
          b_string = ''
          for v1 in lines[1][1]:
            b_string = f'{b_string}{massive_memory.integer_to_massive_memory(int(v1, base=16))}'
          b_string = b_string.ljust(12288, "A")
          b_f.write(f"AAA{b_string}")

      if v == 'c':
        with open(f'{fp_cm2}/c', 'wt') as c_f:
          c_string = ''
          for v1 in lines[1][2]:
            c_string = f'{c_string}{massive_memory.integer_to_massive_memory(int(v1, base=16))}'
          c_string = c_string.ljust(12288, "A")
          c_f.write(f"AAA{c_string}")

      if v == 'code':
        with open(f'{fp_cm2}/code', 'wt') as code_f:
          code_f.write(f'00{''.join(lines[1][3]).ljust(8192, '0')}')

  return lines

write_file('output.af', assemble_to_list(program), 'cm2_output')