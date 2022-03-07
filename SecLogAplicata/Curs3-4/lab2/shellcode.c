#include <sys/mman.h>
#include <stdio.h>
#include <string.h>

char shellcode[] = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80\0";

int main()
{
    void* mem = mmap(NULL, 4096, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);
    printf("Allocated at %p.\n", mem);
    
    strcpy(mem, shellcode);
    printf("Copied shellcode into executable memory.\n");

    int (*f)() = mem;

    printf("Running shellcode...\n");
    f();

    return 0;
}