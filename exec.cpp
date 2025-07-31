#include <iostream>
#include <unistd.h>

int main() {
    char* args[] = { (char*)"/bin/ls", (char*)"-l", NULL };
    execv("/bin/ls", args);

    std::cerr << "exec failed.\n"; // Only runs if exec fails
    return 1;
}
