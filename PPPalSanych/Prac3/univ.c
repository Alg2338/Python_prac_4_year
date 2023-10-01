#include <stdio.h>



int FindElement(int a[800]) {
    int N = 800, i = 0, j = N - 1;
    int counter = 0;
    while (1) {
        printf("counter = %d\n", counter++);
        if (j - i == 1) {
            int b = a[i];
            return a[i] + 1;
        }

        int idx = (i + j) / 2;
        if (a[idx] > idx + 50) 
            j = idx;
        else 
            i = idx;
    }
}

int main(void) {
    printf("bfbvfjkvfs");
    int N = 800;
    int a[800];
    for (int i = 0; i < N; ++i) {
        scanf("%d\n", &a[i]);
    }
    printf("bhjfbbvdfhbj");
    printf("res = %d\n", FindElement(a));
    return 0;
}