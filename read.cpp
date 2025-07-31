#include <iostream>
#include <dirent.h>

int main() {
    DIR* dir = opendir(".");
    if (!dir) {
        perror("opendir failed");
        return 1;
    }

    std::cout << "Files in current directory:\n";
    struct dirent* entry;
    while ((entry = readdir(dir)) != NULL) {
        std::cout << entry->d_name << std::endl;
    }

    closedir(dir);
    return 0;
}
