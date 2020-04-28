import random


def main(thisParam, thisNode, thisGroup, app, userEdited):
    knob_name = thisParam.getScriptName()
    if knob_name == 'random_seed':
        for i in range(10):
            blop_transform = 'tblop_' + str(i) 
            node =  thisNode.getNode( blop_transform )
            transform_random( node, thisNode,  i ) 


def transform_random(transform, thisNode, seed):
	center_x = 1920 / 2
	center_y = 1080 / 2

	_seed = ( thisNode.getParam( 'random_seed' ).getValue() + 10 ) + ( seed * 10 )
	random.seed( _seed  )
	x = random.randint( -center_x, center_x )
	y = random.randint( -center_y, center_y ) 

	rotate = random.randint(0, 360) 

	transform.getParam( 'translate' ).set(x, y)
	transform.getParam( 'rotate' ).setValue(rotate)

	transform.getParam( 'center' ).set( center_x, center_y )
