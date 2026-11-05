/* Copyright (c) 2026 Christian Luppi. MIT; see LICENSE. */
#pragma once

#include <stdbool.h>
#include <stddef.h>

typedef struct {
  size_t begin;
  size_t end; /* Exclusive. */
} lane_range;

/* On failure, leave *range unchanged. The result never exceeds count. */
static inline bool lane_partition(size_t count, size_t lanes, size_t lane, lane_range* range) {
  if (range == NULL || lanes == 0 || lane >= lanes) {
    return false;
  }

  const size_t quotient = count / lanes, remainder = count % lanes;
  range->begin = lane * quotient + (lane < remainder ? lane : remainder);
  range->end = range->begin + quotient + (size_t)(lane < remainder);
  return true;
}
