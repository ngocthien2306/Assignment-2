['N00000021' 'B' 'A' 'C' 'D' 'C' 'C' 'D' 'D' 'C' 'C' 'D' 'B' '' 'B' 'A'
 'C' 'B' '' 'A' 'D' 'A' 'A' 'B' 'D' '\n']
import numpy as np

txt = 'NA0000027'
print(any(c.isalpha() for c in txt[1:]))