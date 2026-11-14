# Measured gates on the exported surfaces; points avoid faces by 0.1 mm.
import sys, json, math
from pathlib import Path
import numpy as np, trimesh
R=Path(__file__).resolve().parents[5]; sys.path.insert(0,str(R/'tools/solidworks'))
from sheet import read_stl, inside, shape_stats
out={}
for name in ['link_boxy','idea_a','idea_b','idea_c','fillet_probe','idea_d','idea_e','fillet_e']:
 p=R/'cad/_wip/sw-eval/terra-high-c'/f'{name}.stl'; mesh=trimesh.load(str(p),force='mesh'); tri=read_stl(p)
 out[name]={'watertight':bool(mesh.is_watertight),'components':len(mesh.split()),'volume_mm3':float(mesh.volume),'bounds':mesh.bounds.tolist(),'shape':shape_stats(tri)}
tri=read_stl(R/'cad/_wip/sw-eval/terra-high-c/idea_e.stl')
def test(label,pts,expect=False):
 pts=np.asarray(pts); got=inside(tri,pts,chunk=30); out[label]={'samples':len(pts),'violations':int(np.count_nonzero(got != expect))}
# Cylinders discretised in radius, angle and axis; exclude nominal boundaries.
pts=[]
for k in range(6):
 a=k*math.pi/3; x,z=25*math.cos(a),25*math.sin(a)
 for y in np.linspace(4.1,13.9,8):
  for rad in [0,1.7,3.3]:
   for t in np.linspace(0,2*math.pi,12,endpoint=False): pts.append((x+rad*math.cos(t),y,z+rad*math.sin(t)))
test('driver_clear',pts)
pts=[]
for z in np.linspace(-213,-183.1,35):
 for x in np.linspace(-14.9,14.9,15):
  for y in np.linspace(-15.9,15.9,13): pts.append((x,y,z))
test('slot_clear',pts)
pts=[]
for z in np.linspace(-184,-0.1,95):
 for rad in (0,1.5,2.85):
  for t in np.linspace(0,2*math.pi,12,endpoint=False): pts.append((rad*math.cos(t),rad*math.sin(t),z))
test('cable_clear',pts)
# Bearing annulus: sample just inside each cheek over radii 4.2 to 8.9.
pts=[]
for y in (-16.1,16.1):
 for rad in (4.2,6,8,8.9):
  for t in np.linspace(0,2*math.pi,36,endpoint=False): pts.append((rad*math.cos(t),y,-200+rad*math.sin(t)))
test('cheek_annulus_solid',pts,True)
# Verify flat ring by probing either side, excluding holes and sampling away from boundaries.
pts=[]
for rad in (15.3,18,21,24,27,30.7):
 for t in np.linspace(0,2*math.pi,96,endpoint=False):
  x,z=rad*math.cos(t),rad*math.sin(t)
  if min(math.hypot(x-25*math.cos(k*math.pi/3),z-25*math.sin(k*math.pi/3)) for k in range(6))>1.9: pts.append((x,-3.85,z))
test('mount_ring_inside',pts,True)
test('mount_ring_outside',[(x,-4.15,z) for x,y,z in pts])
print(json.dumps(out,indent=2)); (R/'tools/solidworks/playbook/eval/terra-high-c/mesh_checks.json').write_text(json.dumps(out,indent=2),encoding='utf-8')

