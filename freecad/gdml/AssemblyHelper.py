from __future__ import annotations
#########################################################
#
#   Assembly dictionary
#
#########################################################
# Geant4 generates its own internal names for the
# physical volumes that are included in the assembly.
# The names are of the form
#
# av_WWW_impr_XXX_YYY_ZZZ
#
# where:
# WWW - assembly volume instance number. I gather this is a number that starts
#       at 1 when the first assembly structure is encountered in the gdml file
#       and then is incremented by one every time a new <assembly structure
#       is encountered
# XXX - assembly volume imprint number. A given assembly can be placed inside several logical volume mothers.
#       The imprint number keeps track of how many times the one and same
#       assembly has been placed.
# YYY - the name of the placed logical volume. geant seems to append an '_pv'
#       to our generated logical volume names, which for current exportGDML is
#        'V-' + copied solid name.
#        As of 2024-10-30 The volume name is not necessarily V- + solid name
#        A NameManager class takes care of naming things and the static
#        NameManager.getVolumeName(obj), where obj is the App::Part that has name YYY
# ZZZ - the logical volume index inside the assembly volume. This is a counter
#       that increases sequentially with the number of solids in the assembly
# to keep track of what a bordersurface is replaced by we use the following
# dictionaries. Each has as key the name of the App::Part  that appears
# in the PV1, PV2 properties of the bordersurface
'''
Consider the following section of a gdml file. By feeding
this to load_gdml_color and examining the output the
indicated physvol names were generated

  <solids>
    <box name="WorldBox" x="200.0" y="200.0" z="200.0" lunit="mm"/>
    <tube name="tube" rmin="0.0" rmax="10" startphi="0.0" deltaphi="360.0" aunit="deg" z="10.0" lunit="mm"/>
    <box name="cube" x="10.0" y="10.0" z="10.0" lunit="mm"/>
  </solids>
  <structure>
    <volume name="V-cube">
      <materialref ref="G4_Ge"/>
      <solidref ref="cube"/>
    </volume>
    <volume name="V-tube">
      <materialref ref="G4_NYLON-6-6"/>
      <solidref ref="tube"/>
    </volume>
    <assembly name="assembly1">
	  <!-- the physvol name is irrelevant. Geant will generate its own -->
      <physvol name="ignored1">                               # generated name = av_1_impr_1_V-cube_pv_0
                                                              # www=1   The is the first assembly in the gdml file
                                                              # impr=1  This is the first placement of assembly 1
                                                              # zzz=0   This is the first logical volume in this assembly
        <volumeref ref="V-cube"/>
        <position name="cube_pos1" x="0" y="0" z="0"/>
      </physvol>
      <physvol name="ignored2">                              # generated name = av_1_impr_1_V-tube_pv_1
                                                              # www=1   The is the first assembly in the gdml file
                                                              # impr=1  This is the first place placement of assembly 1
                                                              # zzz=1   This is the second logical volume in this assembly
        <volumeref ref="V-tube"/>
        <position name="cube_pos2" x="50" y="0" z="0"/>
      </physvol>
    </assembly>
    <assembly name="assembly2">
	  <!-- the physvol name is irrelevant. Geant will generate its own -->
      <physvol name="ignored3">                              # generated name = av_2_impr_1_V-cube_pv_0
                                                              # www=2   The is the second assembly in the gdml file
                                                              # impr=1  This is the first place placement of assembly 2
                                                              # zzz=0   This is the first logical volume in this assembly
        <volumeref ref="V-cube"/>
        <position name="cube_pos1" x="0" y="0" z="0"/>
      </physvol>
      <physvol name="ignored4">
        <volumeref ref="V-tube"/>
        <position name="cube_pos2" x="50" y="0" z="0"/>
      </physvol>
    </assembly>
    <volume name="worldVOL">
      <materialref ref="G4_AIR"/>
      <solidref ref="WorldBox"/>
      <physvol name="PV-assembly1">
        <volumeref ref="assembly1"/>
        <positionref ref="center"/>
        <rotationref ref="identity"/>
      </physvol>
      <physvol name="PV-assembly2">
        <volumeref ref="assembly2"/>
        <position name="assembly2_pos" y="30" />
        <rotationref ref="identity"/>
      </physvol>
	  <!-- place assembly1 again, at a different place -->
      <physvol name="PV-assembly3">                        # Note that this results in a second placement of assembly 1
                                                           # The physvol names of this second placement are:
                                                           # av_1_impr_2_V-cube_pv_0   and
                                                           # av_1_impr_2_V-tube_pv_1
                                                           # This is the same names as in physvols of assembly 1, except the
                                                           # imprint number is 2, instead of 1.
        <volumeref ref="assembly1"/>
        <position name="pos3" y="-30"/>
        <rotationref ref="identity"/>
      </physvol>
    </volume>
  </structure>

'''
from dataclasses import dataclass

from .exportGDML import isAssembly, assemblyHeads


class AssemblyHelper:
    maxWww = 0

    def __init__(self, assemblyVol, instCount, imprNum):
        self.assemblyVol = assemblyVol
        self.xxx = imprNum
        self.www = instCount
        if self.www > AssemblyHelper.maxWww:
            AssemblyHelper.maxWww = instCount
        self.solids = []
        self.zzz = 0

    def addSolid(self, obj):
        self.solids.append(obj)

    def getPVname(self, obj, idx=-1) -> str:
        from .exportGDML import NameManager

        if idx == -1:
            idx = self.zzz
            self.zzz += 1
            
        if hasattr(obj, "LinkedObject"):
            obj = obj.LinkedObject
        return (
            "av_"
            + str(self.www)
            + "_impr_"
            + str(self.xxx)
            + "_"
            + NameManager.getVolumeName(obj)
            + "_pv_"
            + str(idx)
        )


class AssemblyTreeNode:
    from .exportGDML import assemblyHeads

    def __init__(self, assemObj, parent):
        self.parent = parent
        self.assemObj = assemObj
        self.assemHeads = assemblyHeads(assemObj)
        self.left_child = None
        self.right_sibling = None

    def insert(self, assemObj):
        if self.assemObj:
            if assemObj in self.assemblyHeads:
                if self.left_child is None:
                    self.left_child = AssemblyTreeNode(assemObj, self)
                else:
                    self.left_child.insert(assemObj)
            else:
                if self.right_sibling is None:
                    self.right_sibling = AssemblyTreeNode(assemObj, self)
                else:
                    self.right_sibling.insert(assemObj)
        else:
            self.assemObj = assemObj
