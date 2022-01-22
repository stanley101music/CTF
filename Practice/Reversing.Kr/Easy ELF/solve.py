import angr
import claripy

proj = angr.Project('./Easy_ELF', load_options={'auto_load_libs': False})


# Construct a scanf function
class ReplaceScanf(angr.SimProcedure):
    
    def run(self, format_str, param):
        scanf = claripy.BVS("", 6*8)
        self.state.memory.store(param, scanf, endness='big')
        self.state.globals["solutions"] = (scanf)


# Symbol hook
scanf_sym = "__isoc99_scanf"
proj.hook_symbol(scanf_sym, ReplaceScanf())

state = proj.factory.entry_state()
simu = proj.factory.simulation_manager(state)

find = 0x0804854F
avoid = 0x0804855B
simu.explore(find=find, avoid=avoid)

if simu.found:
    sol_state = simu.found[0]
    res = sol_state.globals["solutions"]
    flag = sol_state.solver.eval(res, cast_to=bytes)
    print(flag)
else:
    print("Not found!")