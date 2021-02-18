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
}
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
