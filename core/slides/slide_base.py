from slide_common import setup


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    setup(thisParam, thisNode)
