import tkinter as tk
import random

HACKER_CODE = """
struct group_info init_groups = { .usage = ATOMIC_INIT(2) };
struct group_info *groups_alloc(int gidsetsize) {
    struct group_info *group_info;
    int nblocks;
    int i;

    nblocks = (gidsetsize + NGROUPS_PER_BLOCK - 1) / NGROUPS_PER_BLOCK;
    nblocks = nblocks ? : 1;
    group_info = kmalloc(sizeof(*group_info) + nblocks*sizeof(gid_t *), GFP_USER);
    if (!group_info)
        return NULL;
    group_info->ngroups = gidsetsize;
    group_info->nblocks = nblocks;
    atomic_set(&group_info->usage, 1);

    if (gidsetsize <= NGROUPS_SMALL)
        group_info->blocks[0] = group_info->small_block;
    else {
        for (i = 0; i < nblocks; i++) {
            gid_t *b;
            b = (void *)__get_free_page(GFP_USER);
            if (!b)
                goto out_undo_partial_alloc;
            group_info->blocks[i] = b;
        }
    }
    return group_info;
}

// INITIATING OVERRIDE PROTOCOL...
// BYPASSING FIREWALL... 
// ACCESS GRANTED.
// DOWNLOADING CLASSIFIED DATA...
"""

class HackerTyper:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Hacker Console")
        self.root.configure(bg='black')
        self.root.attributes('-fullscreen', True)
        
        self.text_area = tk.Text(self.root, bg='black', fg='#00FF00', 
                               font=("Consolas", 14), borderwidth=0, insertbackground='green')
        self.text_area.pack(fill='both', expand=True)
        
        self.code_index = 0
        self.code_len = len(HACKER_CODE)
        
        self.root.bind("<Key>", self.add_code)
        self.root.bind("<Escape>", lambda e: self.root.destroy())
        
        self.text_area.insert("1.0", "Connecting to server...\n")

    def add_code(self, event):
        if event.keysym == 'Escape': return
        
        chars_to_add = random.randint(3, 8)
        end_index = min(self.code_index + chars_to_add, self.code_len)
        
        chunk = HACKER_CODE[self.code_index:end_index]
        self.text_area.insert(tk.END, chunk)
        self.text_area.see(tk.END)
        
        self.code_index = end_index
        
        if self.code_index >= self.code_len:
            self.code_index = 0
            self.text_area.insert(tk.END, "\n\n// REBOOTING SYSTEM...\n\n")

if __name__ == "__main__":
    HackerTyper()
