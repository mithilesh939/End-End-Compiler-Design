load Multiplier.hdl,
output-file Multiplier.out,
compare-to Multiplier.cmp,
output-list a%B1.16.1 b%B1.16.1 outlow%B1.16.1 outhigh%B1.16.1;

// Test 1: 
set a %B0000000000000000,
set b %B0000000000000000,
eval,
output;

// Test 2: 1 * 1 = 1
set a %B0000000000000001,
set b %B0000000000000001,
eval,
output;

// Test 3: 255 * 255 = 65025
set a %B0000000011111111,
set b %B0000000011111111,
eval,
output;

// Test 4: 256 * 256 = 65536
set a %B0000000100000000,
set b %B0000000100000000,
eval,
output;

// Test 5: Alternating bits
set a %B1010101010101010,
set b %B0101010101010101,
eval,
output;

// Test 6: Max * Max
set a %B1111111111111111,
set b %B1111111111111111,
eval,
output;