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
## signal.c
```C
#include <stdio.h>
#include <unistd.h>
#include <signal.h>

void timeout(int sig) {
    if(sig == SIGALRM) {
        puts("Time out");
    alarm(2);
    }
}

void keycontrol(int sig) {
    if(sig == SIGINT) {
        puts("CTRL+C pressed");
    }
}

int main(int argc, char **argv) {
    int i;
    signal(SIGALRM, timeout);
    signal(SIGINT, keycontrol);
    alarm(2);
    for(i = 0; i < 3; i++) {
        puts("Wait...");
        sleep(100);
    }
    return 0;
}

/*
Wait -> Time out -> Wait -> Time out -> Wait -> Time out 
[0]                 [1]                 [2]
시그널이 발생하면 sleep 함수의 호출로 블로킹 상태에 있던 프로세스가 깨어난다.
*/
```
## sigaction.c
```C
#include <stdio.h>
#include <unistd.h>
#include <signal.h>

void timeout(int sig) {
    if(sig == SIGALRM) {
        puts("Time out");
    alarm(2);
    }
}

int main(int argc, char **argv) {
    int i;
    struct sigaction act;
    act.sa_handler = timeout;
    sigemptyset(&act.sa_mask);
    act.sa_flags = 0;
    sigaction(SIGALRM, &act, 0);
    alarm(2);
    for(i = 0; i < 3; i++) {
        puts("Wait");
        sleep(10);
    }
    return 0;
}

```
## remove_zombie.c
```C
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <sys/wait.h>

void read_childproc(int sig) {
    int status;
    pid_t id = waitpid(-1, &status, WNOHANG);
    if(WIFEXITED(status)) {
        printf("removed proc id: %d\n", id);
        printf("child send: %d\n", WEXITSTATUS(status));
    }
}

int main(int argc, char** argv) {
    pid_t pid;
    struct sigaction act;
    act.sa_handler = read_childproc;
    sigemptyset(&act.sa_mask);
    act.sa_flags = 0;
    sigaction(SIGCHLD, &act, 0);

    pid = fork();
    if(pid == 0) {
        puts("Child process");
        sleep(10);
        return 12;
    } else {
        printf("Child proc id: %d\n", pid);
        pid = fork();
        if(pid == 0) {
            puts("Child process");
            sleep(10);
            exit(24);
        } else {
            int i;
            printf("Child proc: %d\n", pid);
            for(i = 0; i < 5; i++) {
                puts("Wait...");
                sleep(5);
            }
        }
    }
    return 0;
}
```
