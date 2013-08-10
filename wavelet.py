from __future__ import division
from pylab import *

s = arange(16)
#N = length(S);
N = len(s)
#s1 = S(1:2:N-1) + sqrt(3)*S(2:2:N); # 1, 3, 5, 7... and 2, 4, 6, 
i = arange(N/2, dtype=int)*2
s1 = s[i] + sqrt(3) * s[i+1]
#d1 = S(2:2:N) - sqrt(3)/4*s1 - (sqrt(3)-2)/4*[s1(N/2); s1(1:N/2-1)];
w = concatenate(([s1[N/2-1]], s1[0:N/2-1]))
d1 = s[i+1] - sqrt(3)/4*s1 - (sqrt(3)-2)/4*w
#s2 = s1 - [d1(2:N/2); d1(1)];
#s = (sqrt(3)-1)/sqrt(2) * s2;
#d = (sqrt(3)+1)/sqrt(2) * d1;











