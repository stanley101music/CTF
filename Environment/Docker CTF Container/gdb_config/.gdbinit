# peda
define init-peda
source ~/peda/peda.py
set style address foreground green
end

# pwndbg
define init-pwndbg
source /root/pwndbg/gdbinit.py
# banner-color: color for banner line
# default: blue
set banner-color cyan
# memory-heap-color: color for heap memory
# default: blue
set memory-heap-color light-cyan
source ~/Pwngdb/pwngdb.py
source ~/Pwngdb/angelheap/gdbinit.py
define hook-run
python
import angelheap
angelheap.init_angelheap()
end
end
# Change color of addresses to green
set style address foreground green
end

# gef
define init-gef
source ~/.gdbinit-gef.py
theme dereference_register_value bold yellow
theme registers_register_name bold cyan
theme table_heading bold green
set style address foreground green
end