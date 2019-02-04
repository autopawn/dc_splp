import os
import sys
import numpy as np

def get_dirs(dir,ext=None):
    dirs = []
    for subdir in os.listdir(dir):
        subdir_path = os.path.join(dir,subdir)
        if os.path.isdir(subdir_path):
            contents = get_dirs(subdir_path,ext)
            dirs += [[subdir]+x for x in contents]
        else:
            if ext is None or (len(subdir)>=len(ext) and subdir[-len(ext):]==ext):
                dirs += [[subdir]]
    return dirs

def read_optimum(fname):
    fi = open(fname)
    for lin in fi:
        if "#" in lin: continue
        k = lin.split()
    fi.close()
    assigns = [int(x) for x in k[:-1]]
    value = float(k[-1])
    return assigns,value


def read_solution(fname):
    if not os.path.isfile(fname):
        return None,None
    # ---
    fi = open(fname)
    assigns = None
    value = None
    for lin in fi:
        if (assigns is None) and ("Assigns:" in lin):
            assigns = [int(x) for x in lin.split()[1:]]
        if (value is None) and ("Value:" in lin):
            value = -float(lin.split()[1])
        if (assigns is not None) and (value is not None):
            break
    fi.close()
    assert(assigns is not None)
    assert(value is not None)
    #
    return assigns,value

def is_optimum(sol,opt):
    opt_assi,opt_val = opt
    sol_assi,sol_val = sol
    if sol_assi is None:
        assert(sol_val is None)
        return False
    sol_facts = set(sol_assi)
    opt_facts = set(opt_assi)
    if sol_facts == opt_facts: return True
    if sol_val <= opt_val: return True
    return False

prob_dir = "splp"
sols_dir = sys.argv[1] if len(sys.argv)>=2 else "res/n_200_400/splp"

problems = {}
problems['opt'] = get_dirs(prob_dir,".opt")
problems['bub'] = get_dirs(prob_dir,".bub")

max_facilities = 0
max_clients = 0

summary = {}
for kind in ('opt','bub'):
    summary[kind] = []
    print("="*80)
    print("> PROBLEMS: "+kind.upper())
    print("="*80)
    prob_names = sorted(list(problems[kind]))
    #
    group_names = set([x[0] for x in prob_names])

    for group in group_names:
        group_prob_names = [x for x in prob_names if x[0]==group]

        strings = []
        optis = 0
        nones = 0
        perces = []

        for prob in group_prob_names:
            joined = os.path.join(*prob)
            fname = os.path.join(prob_dir,joined)
            opt_data = read_optimum(fname)
            # --- Maximums
            n_opt_facilities = len(set(opt_data[0]))
            n_clients = len(opt_data[0])
            max_facilities = max(max_facilities,n_opt_facilities)
            max_clients = max(max_clients,n_clients)
            # --- Get the solution
            sol_fname = os.path.join(sols_dir,joined)
            sol_fname = sol_fname[:-4]+"_ls"
            sol_data = read_solution(sol_fname)
            # --- Check for optimality
            if sol_data[0] is None:
                show = None
            else:
                opt = is_optimum(sol_data,opt_data)
                if opt:
                    show = 1
                else:
                    show = 0
            perce = 0 if sol_data[1] is None else sol_data[1]/opt_data[1]
            if show==1:
                optis += 1
            elif show==0:
                strings.append("%-40s %5s %5d %5d %12.3f %12.3f %8.4f"%(
                    joined,show,n_clients,n_opt_facilities,sol_data[1] or 0,opt_data[1],perce))
                perces.append(perce)
            else:
                nones += 1

        print("-"*20)
        perce = "  --  " if len(perces)==0 else "%9.6f"%(np.mean(perces))
        print("%-40s opt:%3d/%-3d   nons:%3d/%-3d perce:%s"%(group,optis,len(group_prob_names),nones,len(group_prob_names),perce))
        for stri in strings:
            print(stri)

print("max_opt_facilities %d"%max_facilities)
print("max_clients %d"%max_clients)