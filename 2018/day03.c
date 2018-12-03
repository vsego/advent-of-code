#include <stdio.h>
#include <stdlib.h>

void add_claim(int **claims, char claim[23]) {
    int l, t, w, h, r, b;

    sscanf(claim, "#%*d @ %d,%d: %dx%d", &l, &t, &w, &h);
    r = l + w;
    b = t + h;
    for (int i = l; i < r; i++)
        for (int j = t; j < b; j++)
            claims[i][j]++;
}

int check_claim(int **claims, char claim[23]) {
    int id, l, t, w, h, r, b;

    sscanf(claim, "#%d @ %d,%d: %dx%d", &id, &l, &t, &w, &h);
    r = l + w;
    b = t + h;
    for (int i = l; i < r; i++)
        for (int j = t; j < b; j++)
            if (claims[i][j] > 1) return 0;
    return id;
}

int **init(int w, int h) {
    int **claims;

    claims = (int**)malloc(sizeof(int*) * w);
    for (int i = 0; i < w; i++) {
        claims[i] = (int*)malloc(sizeof(int) * h);
        for (int j = 0; j < h; j++)
            claims[i][j] = 0;
    }
    return claims;
}

void finish(int **claims, int w, int h) {
    for (int i = 0; i < w; i++)
        free(claims[i]);
    free(claims);
}

int count_overlaps(int** claims, int w, int h) {
    int cnt = 0;
    for (int i = 0; i < w; i++)
        for (int j = 0; j < h; j++)
            if (claims[i][j] > 1)
                cnt++;
    return cnt;
}

void test(void) {
    int **claims, result;

    claims = init(8, 8);
    add_claim(claims, "#1 @ 1,3: 4x4");
    add_claim(claims, "#2 @ 3,1: 4x4");
    add_claim(claims, "#3 @ 5,5: 2x2");
    result = count_overlaps(claims, 8, 8);
    printf("Test 1: %d (%s)\n", result, result == 4 ? "ok" : "failed");
    finish(claims, 8, 8);
}

void part1(int** claims, int w, int h) {
    FILE *fp;
    char line[29];

    fp = fopen("day03.in", "rt");
    while (!feof(fp)) {
        fscanf(fp, "%[^\n]\n", line);
        add_claim(claims, line);
    }
    printf("Part 1: %d\n", count_overlaps(claims, w, h));
}

void part2(int** claims, int w, int h) {
    FILE *fp;
    char line[29];
    int id;

    fp = fopen("day03.in", "rt");
    while (!feof(fp)) {
        fscanf(fp, "%[^\n]\n", line);
        id = check_claim(claims, line);
        if (id) {
            printf("Part 2: %d\n", id);
            return;
        }
    }
    printf("Part 2: whoops\n");
}

int main(void) {
    int w = 1000, h = 1000, **claims;

    test();
    claims = init(w, h);
    part1(claims, w, h);
    part2(claims, w, h);
    finish(claims, w, h);

    return 0;
}
