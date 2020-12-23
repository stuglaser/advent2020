#include <stdio.h>

#define TOP 1000000
void main() {
    int input[] = {3, 9, 4, 6, 1, 8, 5, 2, 7};
    int after[TOP + 1];
    after[0] = -999;
    for (int i = 0; i < 9; ++i) {
        after[input[i]] = input[i + 1];
    }
    after[input[8]] = 10;
    for (int i = 10; i < TOP; ++i) {
        after[i] = i + 1;
    }
    after[TOP] = input[0];

    int at = input[0];
    for (int i = 0; i < 10000000; ++i) {
        int taken_first = after[at];
        int taken_middle = after[taken_first];
        int taken_last = after[taken_middle];

        int place = at > 1 ? at - 1 : TOP;
        while (place == taken_first || place == taken_middle || place == taken_last) {
            place -= 1;
            if (place < 1)
                place = TOP;
        }

        // Trims out taken
        after[at] = after[taken_last];

        // Places taken elements just after `place`
        after[taken_last] = after[place];
        after[place] = taken_first;

        // Advance
        at = after[at];
    }

    long star1 = after[1];
    long star2 = after[star1];
    printf("Part 2: %ld * %ld = %ld\n", star1, star2, star1 * star2);
}
