# Calculate Wilson loop and lattice spacing

Use the WILSLP package to calculate the wilson loop. This package is related to wilslp.cc and inline_wilslp.cc.

### About the "kind" argument in the ini.xml

The "kind" argument in the ini.xml is used to determine the type of the wilson loop to calculate. 

There are three types of wilson loops:
- "space-like" planar Wilson loops
- "time-like" planar Wilson loops
- "time-like" off-axis Wilson loops

The "kind" argument is a integer, but should be converted to binary, and each bit is used to determine whether to calculate that type of the wilson loop.

For example, if we want to calculate the "time-like" planar Wilson loops, we should set the "kind" argument to 2, which is 010 in binary. The first bit (0) is for "space-like" planar Wilson loops, the second bit (1) is for "time-like" planar Wilson loops, the third bit (0) is for "time-like" off-axis Wilson loops.

If we set the "kind" argument to 7, which is 111 in binary, we will calculate all three kinds of Wilson loops.

### Calculate the wilson loop data

- wloop1 is "space-like" planar Wilson loops
- wloop2 is "time-like" planar Wilson loops, note the lengtht = nt / 2
- wloop3 is "time-like" off-axis Wilson loops

For wloop2, each line in the out.xml has the fixed $n_r$ and varying $n_t$.

### Fit the lattice spacing

We know that
$$ W(n_t, n_z) = C \cdot \exp({-n_t} \cdot aV(n_z a) ) $$
in which
$$ aV(n_z a) = Aa + \frac{B}{n_z} + \sigma a^2 n_z $$
because of 
$$ \frac{1}{4a^2} = \frac{1.65 + B}{\sigma a^2} $$
so we got the fit function as
$$ aV(n_z a) =  Aa + \frac{B}{n_z} + 4a^2(1.65 + B) n_z $$


Thus, firstly we use the Wilson loops to calculate linear potential $aV(n_z a)$ with 
$$ aV(n_z a) = \log( W(n_t) / W(n_t + 1) ) $$
then we fit the linear potential to get the lattice spacing $a$.