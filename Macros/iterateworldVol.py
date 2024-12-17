import FreeCAD as App
import FreeCADGui
from PySide import QtGui


def treeView(item, indent: int):
    # breakpoint()
    tab = ""
    for i in range(indent):
        tab += " "
    print(f"{tab} {item.text(0)}")
    for i in range(item.childCount()):
        childItem = item.child(i)
        treeLabel = childItem.text(0)
        try:
            FreeCADobject = App.ActiveDocument.getObjectsByLabel(treeLabel)[0]
            objType = FreeCADobject.TypeId
            if objType != "App::Origin" and objType != "Sketcher::SketchObject":
                treeView(childItem, indent + 4)
        except Exception as e:
            print(e)
            treeLabel = item.text(0)
            print(f"Tree Label: {treeLabel}")
            FreeCADobject = None

    return


# Get world volume from document tree widget
tree = FreeCADGui.getMainWindow().findChildren(QtGui.QTreeWidget)[0]
it = QtGui.QTreeWidgetItemIterator(tree)
sel = FreeCADGui.Selection.getSelection()
doc = FreeCAD.ActiveDocument
found = False

worldVol = sel[0]

for nextObject in it:
    item = nextObject.value()
    treeLabel = item.text(0)
    if not found:
        if treeLabel != doc.Label:
            continue

    if not found:
        print(f"Found current document: {doc.Label}")
    found = True
    try:
        objs = App.ActiveDocument.getObjectsByLabel(treeLabel)
        if len(objs) == 0:
            continue
        objLabel = objs[0].Label
        # treeView(item, 0)
        if objLabel == worldVol.Label:
            # we presume first app part is world volume
            treeView(item, 0)
            break
    except Exception as e:
        print(e)
        FreeCADobject = None

