#include <iostream>
#include <sys/stat.h>

int main() {
    struct stat st;

    if (stat("sample.txt", &st) < 0) {
        perror("Stat failed");
        return 1;
    }

    std::cout << "Size: " << st.st_size << " bytes\n";
    std::cout << "Inode: " << st.st_ino << "\n";
    std::cout << "Permissions: " << std::oct << (st.st_mode & 0777) << "\n";

    return 0;
}
