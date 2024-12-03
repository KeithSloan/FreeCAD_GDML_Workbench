import FreeCADGui

def isParent(parentObj, obj):
    parentsList = obj.Parents
    for parentTuple in parentsList:
        parent = parentTuple[0]
        if parent == parentObj:
            return True
    return False


def buildDocTree():
    childObjects = {}

    def addDaughters(object):
        if object not in childObjects:
            childObjects[object] = []
        for ch in object.OutList:
            objType = ch.TypeId
            if objType != "App::Origin" and objType != "Sketcher::SketchObject":
                if isParent(object, ch):
                    childObjects[object].append(ch)
                addDaughters(ch)
        return

    sel = FreeCADGui.Selection.getSelection()
    worldVol = sel[0]

    addDaughters(worldVol)

    return childObjects

#docTree = buildDocTree()

def printTree():
    for obj in docTree:
        print(obj.Label)
        s = ""
        for ob in docTree[obj]:
            s += ob.Label + ", "
        print(f"\t {s}")

sel = FreeCADGui.Selection.getSelection()
worldVol = sel[0]
doc = FreeCAD.ActiveDocument
parents = {}
for obj in doc.findObjects():
    par = obj.Parents
    if len(par) == 0 and obj != worldVol:
        continue
    else:
        parents[obj.Label] = par

for label in parents:
    s = ""
    for parent in parents[label]:
        s += parent[0].Label + " "
    print(f"{label}: [{s}]")


