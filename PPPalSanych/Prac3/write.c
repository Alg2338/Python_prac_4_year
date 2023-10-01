#include <stdio.h>


int main(void) {
    int x;
    scanf("%d", &x);
    for (int i = 50; i <= 850; ++i) {
        if (i != x) {
            printf("%d\n", i);
        }
    }
    return 0;
}