from project import testing


testing(
    app=app,
    project='/home/pancho/Desktop/test/comp/test.ntp',
    slide_range=[0, 5],
    format=2,  # quarter, half, hd, 4k
    speed=0  # Slow, Normal, Fast
)
