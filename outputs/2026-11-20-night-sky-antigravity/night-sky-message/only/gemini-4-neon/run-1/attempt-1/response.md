The hidden message in [night-sky.png](file:///tmp/vellery-e8ysuiwf/work/night-sky.png) says:

> **THE MONSTER ACTS ON THE MOONSHINE MODULE**

### How it is encoded
The 40 stars in the sky (ordered left-to-right from `x ≈ 23.5` to `x ≈ 778.5`, excluding the shooting star) encode one character each via their vertical (`y`) coordinate in 5-pixel increments:

- `y = 29.5` → `0` (space)
- `y = 29.5 + 5 × n` → `n`-th letter of the alphabet (`1 = A`, `2 = B`, …, `26 = Z`)

Decoding all 40 star `y`-positions left-to-right produces:
`[20, 8, 5, 0, 13, 15, 14, 19, 20, 5, 18, 0, 1, 3, 20, 19, 0, 15, 14, 0, 20, 8, 5, 0, 13, 15, 15, 14, 19, 8, 9, 14, 5, 0, 13, 15, 4, 21, 12, 5]` → **`THE MONSTER ACTS ON THE MOONSHINE MODULE`**.
