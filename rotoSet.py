from __future__ import division

import nuke


def frame_range_setter(selNode):
    """This function sets the frame range of roto shapes based on keys"""
    for selShape in selNode['curves'].getSelected():
        keyFrame = selShape[0].center.getControlPointKeyTimes()
        keyFrames = [int(i) for i in keyFrame]
        low = (min(keyFrames))
        high = (max(keyFrames))
        ### applying min max keyframe to per shape lifetime
        selNode['lifetime_type'].setValue(4)
        selNode['lifetime_start'].setValue(low)
        selNode['lifetime_end'].setValue(high)


def change_selection(node, shapes):
    shapes.setFlag(nuke.rotopaint.FlagType.eSelectedFlag, True)
    node['curves'].changed()
    frame_range_setter(node)
    shapes.setFlag(nuke.rotopaint.FlagType.eSelectedFlag, False)


def progress_bar():
    nodes = nuke.selectedNodes()
    if not nodes == []:
        for node in nodes:
            count = 1
            name = node['name'].value()
            task = nuke.ProgressTask(name)
            task.setMessage('Running')
            if node.Class() == 'Roto':
                nuke.show(node)
                shape_in_layers = node['curves'].rootLayer
                num_of_shapes = len(shape_in_layers)
                for shapes in shape_in_layers:
                    if task.isCancelled():
                        break
                    count = count + 1
                    change_selection(node, shapes)
                    task.setProgress(int((count / num_of_shapes) * 100))
                node.hideControlPanel()
                if task.isCancelled():
                    break

    else:
        nuke.message('Select Roto Nodes')


progress_bar()
