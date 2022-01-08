import cadquery as cq

from lib import cqlib
from projects.a320.tmp.switches import tactile_led
from projects.a320.tmp.btn_mount import btn_mount

cqlib.setup(locals())

result = (
    cq.Assembly()
    .add(tactile_led, name='tactile_led', color=cq.Color('azure2'))
    .add(btn_mount, name='btn_mount', color=cq.Color('blue4'))
    .constrain('tactile_led?mount_top', 'btn_mount?mount_bottom', 'Plane',)
)

result.solve()
result.show('Assembly')

