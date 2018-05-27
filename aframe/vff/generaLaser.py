import math

max_range = 10

for i in range(180):
    i += 180
    x = -max_range*math.sin(math.radians(i))
    y = max_range*math.cos(math.radians(i))
    print("<a-entity id=\"line"+str(i-180)+"\" line=\"start: 2.487 0.431 0; end:",x," 0.431 ",y,"; color: blue\"></a-entity>")
