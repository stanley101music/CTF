import angr


# Create a Pro --> Create a simu --> Explore
pro = angr.Project("./chall")

init_state = pro.factory.entry_state()  # start() addr
simu = pro.factory.simgr(init_state)

good_addr = 0x403d8b
bad_addr = [0x403d24, 0x403dd4]
simu.explore(find=good_addr, avoid=bad_addr)

# get res
if simu.found:
    res = simu.found[0]
    for i in range(3):
        # print stdin/stdout/stderr, stdin is flag
        print(res.posix.dumps(i))
else:
    print("No result!")