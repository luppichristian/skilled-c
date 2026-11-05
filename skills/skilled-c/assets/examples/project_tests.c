/* Copyright (c) 2026 Christian Luppi. MIT license; see LICENSE. */
#include "unity.h"

/* Replace this function with the project code being tested. */
static int clamp_nonnegative(int value) {
  return value < 0 ? 0 : value;
}

void setUp(void) {
}
void tearDown(void) {
}

static void test_clamp_nonnegative(void) {
  TEST_ASSERT_EQUAL_INT(0, clamp_nonnegative(-1));
  TEST_ASSERT_EQUAL_INT(0, clamp_nonnegative(0));
  TEST_ASSERT_EQUAL_INT(3, clamp_nonnegative(3));
}

int main(void) {
  UNITY_BEGIN();
  RUN_TEST(test_clamp_nonnegative);
  return UNITY_END();
}
