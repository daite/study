# Process
## fork.c
```C
#include <stdio.h>
#include <unistd.h>

int gval = 10;
int main(int argc, char* argv[]) {
    pid_t pid;
    int lval = 20;
    gval++;
    lval += 5;
    pid = fork();
    if(pid == 0) {
        gval += 2, lval += 2;
    } else {
        gval -= 2, lval -= 2;
    }
    if(pid == 0) {
        printf("Child proc: [%d, %d]\n", gval, lval);
    } else {
        printf("Parent proc: [%d, %d]\n", gval, lval);
    }
    return 0;
}
/*
Parent proc: [9, 23]
Child proc: [13, 27]
Parent process forks child process by using fork function.
if pid is 0, it is a child process.
*/
```
## zombie.c
```C
#include <stdio.h>
#include <unistd.h>

int main(int argc, char* argv[]) {
    pid_t pid = fork();
    if(pid == 0) {
        puts("Child process");
    } else {
        printf("Child process ID: %d\n", pid);
        sleep(30);
    }
    if(pid == 0) {
        puts("End child process");
    } else {
        puts("End parent process");
    }
    return 0;
}
/*
This example shows that child process ends first, 
and the parent process is waiting for 30 sec for termination.
During this time, the child process's state is zombie.
zombie will be terminated when the parent process is terminated.
*/
```
## wait.c
```C
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main(int argc, char* argv[]) {
    int status;
    pid_t pid = fork();
    if(pid == 0) {
        sleep(6);
        return 3;
    } else {
        printf("Child PID: %d\n", pid);
        pid = fork();
        if(pid == 0) {
            exit(7);
        } else {
            printf("Child PID: %d\n", pid);
            wait(&status); 
            if(WIFEXITED(status)){
                printf("Child send one: %d\n", WEXITSTATUS(status));
            }
            wait(&status);
            if(WIFEXITED(status)){
                printf("Child send one: %d\n", WEXITSTATUS(status));
            }
            sleep(10);
        }
    }
    return 0;
}
/*
This example show that parent process is waiting for child process before termination.
*/
```
## waitpid.c
```C
#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>

int main(int argc, char* argv[]) {
    int status;
    pid_t pid = fork();
    if(pid == 0) {
        sleep(10);
        return 24;
    } else {
        while(!waitpid(-1, &status, WNOHANG)) {
            sleep(3);
            puts("Sleep 3 secs.");
        }
        if(WIFEXITED(status)){
            printf("Child send %d\n", WEXITSTATUS(status));
        }
    }
    return 0;
}
```
