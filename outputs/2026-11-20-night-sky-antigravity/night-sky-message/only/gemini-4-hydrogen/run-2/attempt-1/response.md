The hidden message in [night-sky.png](file:///tmp/vellery-gpm8p_cc/work/night-sky.png) says:

> **THE MONSTER ACTS ON THE MOONSHINE MODULE**

### How it is encoded
The 40 stars across the sky (excluding the diagonal shooting star) encode one character each from left to right via their vertical `y` center coordinate (spaced in 5-pixel increments starting at `y = 29.5`):

$$\text{value} = \frac{y - 29.5}{5}$$

where `0` (`y = 29.5`) is a space and `1`–`26` map to `A`–`Z` (e.g., `y = 129.5` $\rightarrow 20 =$ `T`, `y = 69.5` $\rightarrow 8 =$ `H`, `y = 54.5` $\rightarrow 5 =$ `E`, etc.).
