import turtle as t
t.speed(0)
t.pu()
g=50
b=8
sx=-200
sy=200
for a in range(b):
    t.pu()
    for c in range(b):
        x=sx+c*g
        y=sy-a*g
        if(a+c)%2==0:
            t.fillcolor("white")
        else:
            t.fillcolor("black")
        t.goto(x,y)
        t.pd()
        t.begin_fill()
        for _ in range(4):
            t.forward(g)
            t.right(90)
            t.pd()
        t.end_fill()
