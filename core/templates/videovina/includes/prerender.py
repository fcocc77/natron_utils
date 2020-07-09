from slides import get_slides, delete_slide
from develop import update_post_fx


def prerender(thisNode, workarea):

    slide_range = [2, 5]

    keep_slides = range(slide_range[0], slide_range[-1] + 1)
    for i, slide in enumerate(get_slides(workarea)):

        if not i in keep_slides:
            delete_slide(workarea, i)

    update_post_fx(thisNode, workarea)
