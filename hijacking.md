# 1. GDB practice

## Source: array.c
```C
// array.c
     1	#include <stdio.h>
     2
     3	void print_array() {
     4	    int my_array[] = {9, 5, 11, 2, 15};
     5	    int i;
     6	    for (i=0; i<5; i++)
     7	        printf("my_array[%d] = %d\n", i, my_array[i]);
     8	}
     9
    10	int main() {
    11	    print_array();
    12	    printf("%s\n", "Done");
    13	}
    14
```
## GDB step command
1. gcc -g array.c -o array
2. gdb array
3. break array.c: 11 
4. run   -> print_array() 함수 실행 전에 멈춘다.
```
// step command practice
(gdb) step  -> print_array() 함수 안으로 들어간다. int my_array[];
   밑의 결과를 보면 실행 직전이므로 0으로 초기화 되어있다.
```
```print_array () at array.c:4
(gdb) p &my_array
$1 = (int (*)[5]) 0x7fffffffe380
(gdb) x/16xb $rsp
0x7fffffffe380:	0x00	0x00	0x00	0x00	0x00	0x00	0x00	0x00
0x7fffffffe388:	0x00	0x00	0x00	0x00	0x00	0x00	0x00	0x00
```
```
(gdb) step
6	for (i=0; i<5; i++)
(gdb) x/16xb $rsp
0x7fffffffe380:	0x09	0x00	0x00	0x00	0x05	0x00	0x00	0x00
0x7fffffffe388:	0x0b	0x00	0x00	0x00	0x02	0x00	0x00	0x00
```
```
// byte 배열을 보니, little endian 방식으로 저장되어 있다.
// word (32bit, 4bytes)로 확인해보면 실제값을 확인 할 수 있다.
0x7fffffffe380:	0x00000009	0x00000005	0x0000000b	0x00000002
0x7fffffffe390:	0x0000000f	0x00005555	0x55555060	0x00005555
```
## GDB next command
```
(gdb) break array.c: 11
Breakpoint 1 at 0x11aa: file array.c, line 11.
(gdb) run
Starting program: /home/kali/array
Breakpoint 1, main () at array.c:11
11	    print_array();
(gdb) next
my_array[0] = 9
my_array[1] = 5
my_array[2] = 11
my_array[3] = 2
my_array[4] = 15
12	    printf("%s\n", "Done");
step command과 다르게 함수를 실행 완료 후 printf 함수 실행 전 멈춘다.
```
## GDB continue command
```
(gdb) break array.c: 4
Breakpoint 1 at 0x114d: file array.c, line 4.
(gdb) break array.c: 7
Breakpoint 2 at 0x1179: file array.c, line 7.
(gdb) run
Starting program: /home/kali/array
Breakpoint 1, print_array () at array.c:4
4	    int my_array[] = {9, 5, 11, 2, 15};
(gdb) continue -> 다음 breakpoint인 line 7로 이동한다.
Continuing.

Breakpoint 2, print_array () at array.c:7
7	        printf("my_array[%d] = %d\n", i, my_array[i]);
(gdb) next
my_array[0] = 9
6	    for (i=0; i<5; i++)
(gdb) next

Breakpoint 2, print_array () at array.c:7
7	        printf("my_array[%d] = %d\n", i, my_array[i]);
(gdb) next
my_array[1] = 5
6	    for (i=0; i<5; i++)
```
```
(gdb) x/32xw &my_array
0x7fffffffe380:	0x00000009	0x00000005	0x0000000b	0x00000002
0x7fffffffe390:	0x0000000f	0x00005555	0x55555060	0x00005555
0x7fffffffe3a0:	0xffffe3b0	0x00007fff	0x555551b4	0x00005555
0x7fffffffe3b0:	0x555551d0	0x00005555	0xf7e16d0a	0x00007fff
0x7fffffffe3c0:	0xffffe4a8	0x00007fff	0x00000000	0x00000001
0x7fffffffe3d0:	0x555551a6	0x00005555	0xf7e167cf	0x00007fff
0x7fffffffe3e0:	0x00000000	0x00000000	0x4e082419	0x4ecbe305
0x7fffffffe3f0:	0x55555060	0x00005555	0x00000000	0x00000000
(gdb) continue // continue 다음 breakpoint가 없으므로 그 뒤 실행 후 프로그램을 종료한다.
Continuing.
my_array[0] = 9
my_array[1] = 5
my_array[2] = 11
my_array[3] = 2
my_array[4] = 15
Done
[Inferior 1 (process 5221) exited normally]
```
## GDB command disass
```
(gdb) disass main
Dump of assembler code for function main:
   0x00005555555551a6 <+0>:	push   %rbp
   0x00005555555551a7 <+1>:	mov    %rsp,%rbp
   0x00005555555551aa <+4>:	mov    $0x0,%eax
   0x00005555555551af <+9>:	call   0x555555555145 <print_array>
   0x00005555555551b4 <+14>:	lea    0xe5c(%rip),%rdi        # 0x555555556017
   0x00005555555551bb <+21>:	call   0x555555555030 <puts@plt>
   0x00005555555551c0 <+26>:	mov    $0x0,%eax
   0x00005555555551c5 <+31>:	pop    %rbp
   0x00005555555551c6 <+32>:	ret
End of assembler dump.
```
# 2. Memory region for programming
```C
 // mem_region.c
     1	#include <stdio.h>
     2	#include <stdlib.h>
     3
     4	int my_global_var = 99;
     5
     6	int add(int a) {
     7	    int b = a + my_global_var;
     8	    return b;
     9	}
    10
    11	int main() {
    12	    int *ptr = (int *)malloc(sizeof(int) * 3);
    13	    ptr[0] = 0;
    14	    ptr[1] = 1;
    15	    ptr[2] = add(1);
    16	    printf("ptr[0] = %d, ptr[1] = %d, ptr[2] = %d\n", ptr[0], ptr[1], ptr[2]);
    17	    return 0;
    18	}
```
## [memory region](https://courses.engr.illinois.edu/cs225/fa2020/resources/stack-heap/)
```
$1 = (int *) 0x555555558038 <my_global_var> ; data region
(gdb) p &b
$2 = (int *) 0x7fffffffe36c ; stack region
(gdb) continue
Continuing.

Breakpoint 2, main () at mem_region.c:16
16	    printf("ptr[0] = %d, ptr[1] = %d, ptr[2] = %d\n", ptr[0], ptr[1], ptr[2]);
(gdb) p ptr
$3 = (int *) 0x5555555592a0 ; heap region
```
```
// main 함수가 add 함수 보다 stack에 먼저 PUSH됨을 확인
Breakpoint 1, add (a=1) at mem_region.c:8
8	    return b;
(gdb) p &b
$1 = (int *) 0x7fffffffe36c
(gdb) continue
Continuing.

Breakpoint 2, main () at mem_region.c:18
18	    printf("ptr[0] = %d, ptr[1] = %d, ptr[2] = %d\n", ptr[0], ptr[1], ptr[2]);
(gdb) p &a
$2 = (int *) 0x7fffffffe38c
```
## stackframe check
```C
     1	#include <stdio.h>
     2
     3	long func(long a, long b) {
     4	    long x = 0;
     5	    long y = 0;
     6	    x  = a * a;
     7	    y  = b * b;
     8
     9	    return x + y;
    10	}
    11
    12	int main() {
    13	    long z = func(3, 5);
    14	    printf("3^2 + 5^2 = %d\n", z);
    15	    return 0;
    16	}
```
* X86_64의 경우 함수의 매개변수 1~6은 차례로 레지스터 **rdi, rsi, rdx, r10, r8, r9** 에 저장된다.
```
Breakpoint 1, func (a=3, b=5) at stack_frame_check.c:4
4	    long x = 0;
(gdb) p $rdi
$1 = 3
(gdb) p $rsi
$2 = 5
```
```
(gdb) p &x
$3 = (long *) 0x7fffffffe368 // X가 Y보다 먼저 stack에 PUSH;
(gdb) step
6	    x  = a * a;
(gdb) p &y
$4 = (long *) 0x7fffffffe360
gdb) x/32xw $rsp - 64
0x7fffffffe340:	0x00f0b6ff	0x00000000	0x000000c2	0x00000000
0x7fffffffe350:	0x00000005	0x00000000	0x00000003	0x00000000
0x7fffffffe360:	0x00000019	0x00000000	0x00000009	0x00000000
0x7fffffffe370:	0xffffe390	0x00007fff	0x5555518d	0x00005555
0x7fffffffe380:	0xffffe480	0x00007fff	0x00000022	0x00000000
0x7fffffffe390:	0x555551b0	0x00005555	0xf7e16d0a	0x00007fff
0x7fffffffe3a0:	0xffffe488	0x00007fff	0x00000000	0x00000001
0x7fffffffe3b0:	0x55555176	0x00005555	0xf7e167cf	0x00007fff
```
```
(gdb) disass main
Dump of assembler code for function main:
   0x0000555555555176 <+0>:	push   %rbp
   0x0000555555555177 <+1>:	mov    %rsp,%rbp
   0x000055555555517a <+4>:	sub    $0x10,%rsp
   0x000055555555517e <+8>:	mov    $0x5,%esi
   0x0000555555555183 <+13>:	mov    $0x3,%edi
   0x0000555555555188 <+18>:	call   0x555555555135 <func>
   0x000055555555518d <+23>:	mov    %rax,-0x8(%rbp)
=> 0x0000555555555191 <+27>:	mov    -0x8(%rbp),%rax
   0x0000555555555195 <+31>:	mov    %rax,%rsi
   0x0000555555555198 <+34>:	lea    0xe65(%rip),%rdi        # 0x555555556004
   0x000055555555519f <+41>:	mov    $0x0,%eax
   0x00005555555551a4 <+46>:	call   0x555555555030 <printf@plt>
   0x00005555555551a9 <+51>:	mov    $0x0,%eax
   0x00005555555551ae <+56>:	leave
   0x00005555555551af <+57>:	ret
```
```
 0x7fffffffe370:	0xffffe390	0x00007fff	0x5555518d	0x00005555
<---- Lower adderess  Y ---  X  ---  base pointer -- return address -----> higher address
```
# 3. Assembly language
```asm
; hello.asm
section .data
    mytest: db "hello,world", 0xa

section .text
    global _start

_start:
    mov rax, 1
    mov rdi, 1
    mov rsi, mytest
    mov rdx, 12
    syscall

    mov rax, 60
    mov rdi, 1
    syscall
```
* nasm -f elf64 hello.asm -o hello.o
* ld hello.o -o hello
* ./hello
```
┌──(kali㉿kali)-[~/code]
└─$ objdump -D -M intel hello

hello:     file format elf64-x86-64


Disassembly of section .text:

0000000000401000 <_start>:
  401000:	b8 01 00 00 00       	mov    eax,0x1
  401005:	bf 01 00 00 00       	mov    edi,0x1
  40100a:	48 be 00 20 40 00 00 	movabs rsi,0x402000
  401011:	00 00 00
  401014:	ba 0c 00 00 00       	mov    edx,0xc
  401019:	0f 05                	syscall
  40101b:	b8 3c 00 00 00       	mov    eax,0x3c
  401020:	bf 01 00 00 00       	mov    edi,0x1
  401025:	0f 05                	syscall

Disassembly of section .data:

0000000000402000 <mytest>:
  402000:	68 65 6c 6c 6f       	push   0x6f6c6c65
  402005:	2c 77                	sub    al,0x77
  402007:	6f                   	outs   dx,DWORD PTR ds:[rsi]
  402008:	72 6c                	jb     402076 <_end+0x66>
  40200a:	64                   	fs
  40200b:	0a                   	.byte 0xa
 ```
# 4. Shell code
```asm
     1	; remove null bytes
     2	section .data
     3	    mytest: db "hello,world", 0xa
     4
     5	section .text
     6	    global _start
     7
     8	_start:
     9	    mov al, 1
    10	    xor rdi, rdi
    11	    add rdi, 1
    12	    mov rsi, mytest
    13	    xor rdx, rdx
    14	    add rdx, 12
    15	    syscall
    16
    17	    mov al, 60
    18	    xor rdi, rdi
    19	    add rdi, 1
    20	    syscall
```
```
Disassembly of section .text:

0000000000401000 <_start>:
  401000:	b0 01                	mov    al,0x1
  401002:	48 31 ff             	xor    rdi,rdi
  401005:	48 83 c7 01          	add    rdi,0x1
  401009:	48 be 00 20 40 00 00 	movabs rsi,0x402000 //  still have null bytes.
  401010:	00 00 00
  401013:	48 31 d2             	xor    rdx,rdx
  401016:	48 83 c2 0c          	add    rdx,0xc
  40101a:	0f 05                	syscall
  40101c:	b0 3c                	mov    al,0x3c
  40101e:	48 31 ff             	xor    rdi,rdi
  401021:	48 83 c7 01          	add    rdi,0x1
  401025:	0f 05                	syscall

Disassembly of section .data:

0000000000402000 <mytest>:
  402000:	68 65 6c 6c 6f       	push   0x6f6c6c65
  402005:	2c 77                	sub    al,0x77
  402007:	6f                   	outs   dx,DWORD PTR ds:[rsi]
  402008:	72 6c                	jb     402076 <_end+0x66>
  40200a:	64                   	fs
  40200b:	0a                   	.byte 0xa
```
```asm
     1	; hello.asm
     2
     3	section .text
     4	    global _start
     5
     6	_start:
     7	    jmp mycode
     8	    mytext: db "hello,world", 0xa
     9
    10	mycode:
    11	    mov al, 1
    12	    xor rdi, rdi
    13	    add rdi, 1
    14	    lea rsi, [rel mytext]
    15	    xor rdx, rdx
    16	    add rdx, 12
    17	    syscall
    18
    19	    mov al, 60
    20	    xor rdi, rdi
    21	    add rdi, 1
    22	    syscall
```
```
Disassembly of section .text:

0000000000401000 <_start>:
  401000:	eb 0c                	jmp    40100e <mycode>

0000000000401002 <mytext>:
  401002:	68 65 6c 6c 6f       	push   0x6f6c6c65
  401007:	2c 77                	sub    al,0x77
  401009:	6f                   	outs   dx,DWORD PTR ds:[rsi]
  40100a:	72 6c                	jb     401078 <mycode+0x6a>
  40100c:	64 0a      	or     dh,BYTE PTR fs:[rax-0xceb7ff]

000000000040100e <mycode>:
  40100e:	b0 01                	mov    al,0x1
  401010:	48 31 ff             	xor    rdi,rdi
  401013:	48 83 c7 01          	add    rdi,0x1
  401017:	48 8d 35 e4 ff ff ff 	lea    rsi,[rip+0xffffffffffffffe4]        # 401002 <mytext>
  40101e:	48 31 d2             	xor    rdx,rdx
  401021:	48 83 c2 0c          	add    rdx,0xc
  401025:	0f 05                	syscall
  401027:	b0 3c                	mov    al,0x3c
  401029:	48 31 ff             	xor    rdi,rdi
  40102c:	48 83 c7 01          	add    rdi,0x1
  401030:	0f 05                	syscall
```
