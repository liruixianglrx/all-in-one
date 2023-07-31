#include "eco_ext.h"

int in_2d(int *org_array, int org_dim_1, int org_dim_2, int *check_array,
          int check_dim) {
  if (org_dim_2 != check_dim)
    return -1;

  for (int d1 = 0; d1 < org_dim_1; d1++) {
    int check_state = 1;

    for (int d2 = 0; d2 < org_dim_2; d2++) {
      if (org_array[d1 * org_dim_2 + d2] != check_array[d2]) {
        check_state = 0;
        break;
      }
    }

    if (check_state == 1)
      return 1;
  }
  return 0;
}
