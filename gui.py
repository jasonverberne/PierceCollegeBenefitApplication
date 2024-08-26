import menu_gui
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from cerberus import Validator


root = Tk()
root.iconbitmap("images/morpho_didius.ico")
root.title("Faculty Benefits Evaluation Tool")


def verify_action(phrase, function):
    response = messagebox.askyesno("Verify Action", phrase)
    if response == 1:
        top_window = Toplevel()
        top_window.title("Loading...")
        top_window.iconbitmap("images/morpho_partis_thamyris.ico")
        pause_label = Label(top_window, text="Processing.. Please wait.")
        pause_label.grid(row=0, column=0, padx=20, pady=20)
        top_window.update_idletasks()
        
        function()
        
        top_window.destroy()


def verify_action_analysis(phrase, function):
    response = messagebox.askyesno("Verify Action", phrase)
    if response == 1:
        top_window = Toplevel()
        top_window.title("Analyzing data...")
        top_window.iconbitmap("images/morpho_partis_thamyris.ico")
        pause_label = Label(top_window, text="Analyzing... Please wait.")
        pause_label.grid(row=0, column=0, padx=20, pady=20)
        top_window.update_idletasks()
        
        function()
        
        top_window.destroy()


def del_single_stk():
        id_stk = id_stk_del_entry.get()
        term_stk = term_stk_del_entry.get()
        response = messagebox.askyesno("Verify submission", f"You entered:\n\nID: {id_stk}\n\nTerm: {term_stk}\n\nIs that correct?")
        if response == True:
             menu_gui.delete_stacking('single',  id_stk_del_entry.get(), term_stk_del_entry.get())
             top_stk_del.destroy()
        else:
             top_stk_del.destroy()
        

def enter_stack_data():
        id = str(id_entry.get())
        name = name_entry.get()
        term = term_entry.get()
        fte = fte_entry.get()

        schema = {'id_stack': {'minlength': 9, 'maxlength': 9, 'regex': '^[0-9]+$' }, 'term_stack': {'regex': '^[0-9]+$', 'minlength': 4, 'maxlength': 4,}, 'fte_stack': {'regex': '^[0-9.]+$'}}
        document =  {'id_stack': id, 'term_stack': term, 'fte_stack': fte}
        v = Validator(schema)
        true_false = v.validate(document)
        # print(f"ID Type: {type(id)}")
        # print(f"Name Type: {type(name)}")
        # print(f"Term Type: {type(term)}")
        # print(f"FTE Type: {type(fte)}")
        print(true_false)
        print(v.errors)
        if true_false == True:
            response = messagebox.askyesno("Verify submission", f"You entered:\n\nID: {id}\n\nName: {name}\n\nTerm: {term} \n\nFTE: {fte}\n\nIs that correct?")
            if response == True:
                menu_gui.add_stacking(id, name, term, fte)
                top_stk_add.destroy()
            else:
                top_stk_add.destroy()
        if true_false == False:
            messagebox.showerror("Incorrect Format Used", f"You have used a format that is not allowed.\n\nIDs are 9 digits (ie 555443333)\n\nName can be any entry\n\nTerms are 4 digits (ie 2227, 2235, etc)\n\nFTE must be digits, but a period (.) is allowed")

        

def stacking_add_data_func():
    global id_entry
    global name_entry
    global term_entry
    global fte_entry
    global top_stk_add

    top_stk_add = Toplevel()
    top_stk_add.title("Add Stacking Data Form")
    top_stk_add.iconbitmap("images/morpho_diana.ico")

    top_frame = LabelFrame(top_stk_add, text="Add Stacking Data")
    top_frame.grid(row=0, column=0, padx=20, pady=20)

    id_label = Label(top_frame, text="Employee ID:")
    id_label.grid(row=0, column=0)
    id_entry = Entry(top_frame)
    id_entry.grid(row=0, column=1)

    name_label = Label(top_frame, text="Name:")
    name_label.grid(row=1, column=0)
    name_entry = Entry(top_frame)
    name_entry.grid(row=1, column=1)

    term_label = Label(top_frame, text="Term:")
    term_label.grid(row=2, column=0)
    term_entry = Entry(top_frame)
    term_entry.grid(row=2, column=1)

    fte_label = Label(top_frame, text="FTE %:")
    fte_label.grid(row=3, column=0)
    fte_entry = Entry(top_frame)
    fte_entry.grid(row=3, column=1)

    submit_btn = Button(top_frame, text="Submit", command=enter_stack_data)
    submit_btn.grid(row=4, column=0, columnspan=2, sticky='news')

    for widget in top_frame.winfo_children():
        widget.grid_configure(padx=10, pady=10)

    
def stacking_delete_data_func(action):
    if action == 'Single':
        global top_stk_del
        global id_stk_del_entry
        global term_stk_del_entry

        top_stk_del = Toplevel()
        top_stk_del.title("Delete Stacking Data Form")
        top_stk_del.iconbitmap("images/morpho_hecuba_sunse.ico")

        top_stk_del_frame = LabelFrame(top_stk_del, text="Delete Single Stacking Data")
        top_stk_del_frame.grid(row=0, column=0, padx=20, pady=20)

        id_stk_del_label = Label(top_stk_del_frame, text="Employee ID:")
        id_stk_del_label.grid(row=0, column=0)
        id_stk_del_entry = Entry(top_stk_del_frame)
        id_stk_del_entry.grid(row=0, column=1)

        term_stk_del_label = Label(top_stk_del_frame, text="Term:")
        term_stk_del_label.grid(row=1, column=0)
        term_stk_del_entry = Entry(top_stk_del_frame)
        term_stk_del_entry.grid(row=1, column=1)

        submit_btn = Button(top_stk_del_frame, text="Submit", command=lambda: del_single_stk())
        submit_btn.grid(row=4, column=0, columnspan=2, sticky='news')

        for widget in top_stk_del_frame.winfo_children():
            widget.grid_configure(padx=10, pady=10)

    elif action == 'All':
         response = messagebox.askyesno("Verify Action", "*** WARNING ***\n\nThis will clear all stacking data and is irreversible.\n\n Continue?")
         if response == True:
            menu_gui.delete_stacking('all')

         else:
             pass
    else:
        messagebox.showerror("Verify Action", "You must choose 'Single' or 'All'")

def view_stacked():
    top_stack = Toplevel()
    top_stack.title("Stacked Data")
    top_stack.iconbitmap("images/mint_morpho.ico")
    top_stack.geometry("1000x500")

    # Create treeview frame
    tree_frame = Frame(top_stack)
    tree_frame.pack(pady=20)

    # Create Treeview Scrollbar
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)
    my_tree.pack()

    # Configure the scrollbar
    tree_scroll.config(command=my_tree.yview)

    # Define columns
    my_tree['columns'] = ("Term", "EMPL_ID", "Name", "FTE")

    # Format columns
    my_tree.column("#0", width=0, minwidth=0)
    my_tree.column("Term", width=120, minwidth=20, anchor=CENTER)
    my_tree.column("EMPL_ID", width=120, minwidth=20, anchor=CENTER)
    my_tree.column("Name", width=120, minwidth=20, anchor=CENTER)
    my_tree.column("FTE", width=120, minwidth=20, anchor=CENTER)  

    # Create headings
    my_tree.heading("#0", text="Label")
    my_tree.heading("Term", text="Term", anchor=CENTER)
    my_tree.heading("EMPL_ID", text="EMPL_ID", anchor=CENTER)
    my_tree.heading("Name", text="Name", anchor=CENTER)
    my_tree.heading("FTE", text="FTE", anchor=CENTER)

    # Add data
    records = menu_gui.view_stacking_data()
    count = 0
    for row in records:
        my_tree.insert(parent="", index='end', iid=count, text="Parent", values=(row.term, row.empl_id, row.name, row.fte_percentage))
        count += 1
    my_tree.pack(pady=20)



def view_contract_records(title, action):
    if action == "Single EMPL ID":
        def single_contract(desired_id):
            desired_id_top.destroy()

            top_stack = Toplevel()
            top_stack.title(title)
            top_stack.iconbitmap("images/mint_morpho.ico")
            top_stack.geometry("1200x500")

            # Create treeview frame
            tree_frame = Frame(top_stack)
            tree_frame.pack(pady=20)

            # Create Treeview Scrollbar
            tree_scroll = Scrollbar(tree_frame)
            tree_scroll.pack(side=RIGHT, fill=Y)

            my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)
            my_tree.pack()

            # Configure the scrollbar
            tree_scroll.config(command=my_tree.yview)

            # Define columns
            my_tree['columns'] = ("Term", "EMPL_ID", "Name", "Contract_Type", "Class_Number", "Subject", "Catalog", "FTE", "Total_Pay")

            # Format columns
            my_tree.column("#0", width=0, minwidth=0)
            my_tree.column("Term", width=120, minwidth=20, anchor=CENTER)
            my_tree.column("EMPL_ID", width=120, minwidth=20, anchor=CENTER)
            my_tree.column("Name", width=120, minwidth=20, anchor=CENTER)
            my_tree.column("Contract_Type", width=120, minwidth=20, anchor=CENTER) 
            my_tree.column("Class_Number", width=120, minwidth=20, anchor=CENTER)
            my_tree.column("Subject", width=120, minwidth=20, anchor=CENTER)    
            my_tree.column("Catalog", width=120, minwidth=20, anchor=CENTER)  
            my_tree.column("FTE", width=120, minwidth=20, anchor=CENTER)  
            my_tree.column("Total_Pay", width=120, minwidth=20, anchor=CENTER)  
            my_tree.column("FTE", width=120, minwidth=20, anchor=CENTER)  

            # Create headings
            my_tree.heading("#0", text="Label")
            my_tree.heading("Term", text="Term", anchor=CENTER)
            my_tree.heading("EMPL_ID", text="EMPL_ID", anchor=CENTER)
            my_tree.heading("Name", text="Name", anchor=CENTER)
            my_tree.heading("Contract_Type", text="Contract Type", anchor=CENTER)
            my_tree.heading("Class_Number", text="Class Number", anchor=CENTER)
            my_tree.heading("Subject", text="Subject", anchor=CENTER)
            my_tree.heading("Catalog", text="Catalog", anchor=CENTER)
            my_tree.heading("FTE", text="FTE", anchor=CENTER)
            my_tree.heading("Total_Pay", text="Total Pay", anchor=CENTER)
            records = menu_gui.view_contract_single_emplid_records(desired_id)
            count = 0
            for row in records:
                my_tree.insert(parent="", index='end', iid=count, text="Parent", values=(row.term, row.empl_id, row.name, row.contract_type, row.class_number, row.subject, row.catalog, row.fte_percentage, row.total_pay))
                count += 1
            my_tree.pack(pady=20)

        desired_id_top = Toplevel()
        desired_id_top.title("Desired ID")
        desired_id_top.iconbitmap("images/Morpho_Achilleana.ico")
        
        desired_id_frame = LabelFrame(desired_id_top, text="EMPL ID to Search")
        desired_id_frame.grid(row=0, column=0, padx=20, pady=10)

        desired_id_label = Label(desired_id_frame, text="EMPL ID: ")
        desired_id_label.grid(row=0, column=0, padx=10, pady=10)

        desired_id_entry = Entry(desired_id_frame)
        desired_id_entry.grid(row=0, column=1, padx=10, pady=10)

        desired_id_submit_button = Button(desired_id_frame, text="Submit", command=lambda: single_contract(desired_id_entry.get()))
        desired_id_submit_button.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

        
    elif action == "All Records":
        top_stack = Toplevel()
        top_stack.title(title)
        top_stack.iconbitmap("images/mint_morpho.ico")
        top_stack.geometry("1200x500")

        # Create treeview frame
        tree_frame = Frame(top_stack)
        tree_frame.pack(pady=20)

        # Create Treeview Scrollbar
        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)
        my_tree.pack()

        # Configure the scrollbar
        tree_scroll.config(command=my_tree.yview)

        # Define columns
        my_tree['columns'] = ("Term", "EMPL_ID", "Name", "Contract_Type", "Class_Number", "Subject", "Catalog", "FTE", "Total_Pay")

        # Format columns
        my_tree.column("#0", width=0, minwidth=0)
        my_tree.column("Term", width=120, minwidth=20, anchor=CENTER)
        my_tree.column("EMPL_ID", width=120, minwidth=20, anchor=CENTER)
        my_tree.column("Name", width=120, minwidth=20, anchor=CENTER)
        my_tree.column("Contract_Type", width=120, minwidth=20, anchor=CENTER) 
        my_tree.column("Class_Number", width=120, minwidth=20, anchor=CENTER)
        my_tree.column("Subject", width=120, minwidth=20, anchor=CENTER)    
        my_tree.column("Catalog", width=120, minwidth=20, anchor=CENTER)  
        my_tree.column("FTE", width=120, minwidth=20, anchor=CENTER)  
        my_tree.column("Total_Pay", width=120, minwidth=20, anchor=CENTER)  
        my_tree.column("FTE", width=120, minwidth=20, anchor=CENTER)  

        # Create headings
        my_tree.heading("#0", text="Label")
        my_tree.heading("Term", text="Term", anchor=CENTER)
        my_tree.heading("EMPL_ID", text="EMPL_ID", anchor=CENTER)
        my_tree.heading("Name", text="Name", anchor=CENTER)
        my_tree.heading("Contract_Type", text="Contract Type", anchor=CENTER)
        my_tree.heading("Class_Number", text="Class Number", anchor=CENTER)
        my_tree.heading("Subject", text="Subject", anchor=CENTER)
        my_tree.heading("Catalog", text="Catalog", anchor=CENTER)
        my_tree.heading("FTE", text="FTE", anchor=CENTER)
        my_tree.heading("Total_Pay", text="Total Pay", anchor=CENTER)
        records = menu_gui.view_contract_records()
        count = 0
        for row in records:
            my_tree.insert(parent="", index='end', iid=count, text="Parent", values=(row.term, row.empl_id, row.name, row.contract_type, row.class_number, row.subject, row.catalog, row.fte_percentage, row.total_pay))
            count += 1
        my_tree.pack(pady=20)

    else:
        messagebox.showerror("Verify Action", "You must choose 'Single EMPL ID' or 'All Records'")


def view_final_results_records(title, action):
    if action == "Single EMPL ID":
        def single_contract(desired_id):
            desired_id_top.destroy()

            top_stack = Toplevel()
            top_stack.title(title)
            top_stack.iconbitmap("images/mint_morpho.ico")
            top_stack.geometry("1200x500")

            # Create treeview frame
            tree_frame = Frame(top_stack)
            tree_frame.pack(pady=20)

            # Create Treeview Scrollbar
            tree_scroll = Scrollbar(tree_frame)
            tree_scroll.pack(side=RIGHT, fill=Y)

            my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)
            my_tree.pack()

            # Configure the scrollbar
            tree_scroll.config(command=my_tree.yview)

            # Define columns
            my_tree['columns'] = ("EMPL_ID", "Name", "Eight", "Seven", "Six", "Five", "Four", "Three", "Two", "Current", "Comment")

            # Format columns
            my_tree.column("#0", width=0, minwidth=0)
            my_tree.column("EMPL_ID", width=120, minwidth=20, anchor=CENTER)
            my_tree.column("Name", width=120, minwidth=20, anchor=CENTER)
            my_tree.column("Eight", width=60, minwidth=20, anchor=CENTER)
            my_tree.column("Seven", width=60, minwidth=20, anchor=CENTER) 
            my_tree.column("Six", width=60, minwidth=20, anchor=CENTER)
            my_tree.column("Five", width=60, minwidth=20, anchor=CENTER)    
            my_tree.column("Four", width=60, minwidth=20, anchor=CENTER)  
            my_tree.column("Three", width=60, minwidth=20, anchor=CENTER)  
            my_tree.column("Two", width=60, minwidth=20, anchor=CENTER)  
            my_tree.column("Current", width=60, minwidth=20, anchor=CENTER)  
            my_tree.column("Comment", width=350, minwidth=20, anchor=CENTER)  

            # Create headings
            my_tree.heading("#0", text="Label")
            my_tree.heading("EMPL_ID", text="EMPL_ID", anchor=CENTER)
            my_tree.heading("Name", text="Name", anchor=CENTER)
            my_tree.heading("Eight", text="Eight", anchor=CENTER)
            my_tree.heading("Seven", text="Seven", anchor=CENTER)
            my_tree.heading("Six", text="Six", anchor=CENTER)
            my_tree.heading("Five", text="Five", anchor=CENTER)
            my_tree.heading("Four", text="Four", anchor=CENTER)
            my_tree.heading("Three", text="Three", anchor=CENTER)
            my_tree.heading("Two", text="Two", anchor=CENTER)
            my_tree.heading("Current", text="Current", anchor=CENTER)
            my_tree.heading("Comment", text="Comment", anchor=CENTER)
            records = menu_gui.view_result_single(desired_id)
            count = 0
            for row in records:
                my_tree.insert(parent="", index='end', iid=count, text="Parent", values=(row.empl_id, row.name, row.eight, row.seven, row.six, row.five, row.four, row.three, row.two, row.current, row.comment))
                count += 1
            my_tree.pack(pady=20)

        desired_id_top = Toplevel()
        desired_id_top.title("Desired ID")
        desired_id_top.iconbitmap("images/Morpho_Achilleana.ico")
        
        desired_id_frame = LabelFrame(desired_id_top, text="EMPL ID to Search")
        desired_id_frame.grid(row=0, column=0, padx=20, pady=10)

        desired_id_label = Label(desired_id_frame, text="EMPL ID: ")
        desired_id_label.grid(row=0, column=0, padx=10, pady=10)

        desired_id_entry = Entry(desired_id_frame)
        desired_id_entry.grid(row=0, column=1, padx=10, pady=10)

        desired_id_submit_button = Button(desired_id_frame, text="Submit", command=lambda: single_contract(desired_id_entry.get()))
        desired_id_submit_button.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

        
    elif action == "All Records":
        top_stack = Toplevel()
        top_stack.title(title)
        top_stack.iconbitmap("images/mint_morpho.ico")
        top_stack.geometry("1200x500")

        # Create treeview frame
        tree_frame = Frame(top_stack)
        tree_frame.pack(pady=20)

        # Create Treeview Scrollbar
        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)
        my_tree.pack()

        # Configure the scrollbar
        tree_scroll.config(command=my_tree.yview)

        # Define columns
        my_tree['columns'] = ("EMPL_ID", "Name", "Eight", "Seven", "Six", "Five", "Four", "Three", "Two", "Current", "Comment")

        # Format columns
        my_tree.column("#0", width=0, minwidth=0)
        my_tree.column("EMPL_ID", width=120, minwidth=20, anchor=CENTER)
        my_tree.column("Name", width=120, minwidth=20, anchor=CENTER)
        my_tree.column("Eight", width=60, minwidth=20, anchor=CENTER)
        my_tree.column("Seven", width=60, minwidth=20, anchor=CENTER) 
        my_tree.column("Six", width=60, minwidth=20, anchor=CENTER)
        my_tree.column("Five", width=60, minwidth=20, anchor=CENTER)    
        my_tree.column("Four", width=60, minwidth=20, anchor=CENTER)  
        my_tree.column("Three", width=60, minwidth=20, anchor=CENTER)  
        my_tree.column("Two", width=60, minwidth=20, anchor=CENTER)  
        my_tree.column("Current", width=60, minwidth=20, anchor=CENTER)  
        my_tree.column("Comment", width=350, minwidth=20, anchor=W)  

        # Create headings
        my_tree.heading("#0", text="Label")
        my_tree.heading("EMPL_ID", text="EMPL_ID", anchor=CENTER)
        my_tree.heading("Name", text="Name", anchor=CENTER)
        my_tree.heading("Eight", text="Eight", anchor=CENTER)
        my_tree.heading("Seven", text="Seven", anchor=CENTER)
        my_tree.heading("Six", text="Six", anchor=CENTER)
        my_tree.heading("Five", text="Five", anchor=CENTER)
        my_tree.heading("Four", text="Four", anchor=CENTER)
        my_tree.heading("Three", text="Three", anchor=CENTER)
        my_tree.heading("Two", text="Two", anchor=CENTER)
        my_tree.heading("Current", text="Current", anchor=CENTER)
        my_tree.heading("Comment", text="Comment", anchor=CENTER)
        records = menu_gui.view_final_results()
        count = 0
        for row in records:
            my_tree.insert(parent="", index='end', iid=count, text="Parent", values=(row.empl_id, row.name, row.eight, row.seven, row.six, row.five, row.four, row.three, row.two, row.current, row.comment))
            count += 1
            my_tree.pack(pady=20)

    elif action == "Only Records to Review":
        top_stack = Toplevel()
        top_stack.title(title)
        top_stack.iconbitmap("images/mint_morpho.ico")
        top_stack.geometry("1200x500")

        # Create treeview frame
        tree_frame = Frame(top_stack)
        tree_frame.pack(pady=20)

        # Create Treeview Scrollbar
        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)
        my_tree.pack()

        # Configure the scrollbar
        tree_scroll.config(command=my_tree.yview)

        # Define columns
        my_tree['columns'] = ("EMPL_ID", "Name", "Eight", "Seven", "Six", "Five", "Four", "Three", "Two", "Current", "Comment")

        # Format columns
        my_tree.column("#0", width=0, minwidth=0)
        my_tree.column("EMPL_ID", width=120, minwidth=20, anchor=CENTER)
        my_tree.column("Name", width=120, minwidth=20, anchor=CENTER)
        my_tree.column("Eight", width=60, minwidth=20, anchor=CENTER)
        my_tree.column("Seven", width=60, minwidth=20, anchor=CENTER) 
        my_tree.column("Six", width=60, minwidth=20, anchor=CENTER)
        my_tree.column("Five", width=60, minwidth=20, anchor=CENTER)    
        my_tree.column("Four", width=60, minwidth=20, anchor=CENTER)  
        my_tree.column("Three", width=60, minwidth=20, anchor=CENTER)  
        my_tree.column("Two", width=60, minwidth=20, anchor=CENTER)  
        my_tree.column("Current", width=60, minwidth=20, anchor=CENTER)  
        my_tree.column("Comment", width=350, minwidth=20, anchor=W)  

        # Create headings
        my_tree.heading("#0", text="Label")
        my_tree.heading("EMPL_ID", text="EMPL_ID", anchor=CENTER)
        my_tree.heading("Name", text="Name", anchor=CENTER)
        my_tree.heading("Eight", text="Eight", anchor=CENTER)
        my_tree.heading("Seven", text="Seven", anchor=CENTER)
        my_tree.heading("Six", text="Six", anchor=CENTER)
        my_tree.heading("Five", text="Five", anchor=CENTER)
        my_tree.heading("Four", text="Four", anchor=CENTER)
        my_tree.heading("Three", text="Three", anchor=CENTER)
        my_tree.heading("Two", text="Two", anchor=CENTER)
        my_tree.heading("Current", text="Current", anchor=CENTER)
        my_tree.heading("Comment", text="Comment", anchor=CENTER)
        records = menu_gui.view_review_result()
        count = 0
        for row in records:
            my_tree.insert(parent="", index='end', iid=count, text="Parent", values=(row.empl_id, row.name, row.eight, row.seven, row.six, row.five, row.four, row.three, row.two, row.current, row.comment))
            count += 1
            my_tree.pack(pady=20)

    else:
        messagebox.showerror("Verify Action", "You must choose 'Single EMPL ID', 'All Records', or 'Only Records to Review")


def download_report(action):
    if action == 'stacked':
        menu_gui.download_stacked_data()
        messagebox.showinfo("Download Status", "Stacked Data Downloaded")
    if action == 'final':
        menu_gui.download_final_results()
        messagebox.showinfo("Download Status", "Final Results Downloaded")


def current_term():
    top_term = Toplevel()
    top_term.title("Current Term")
    top_term.iconbitmap("images/Morpho_Polyphemus.ico")

    term_frame = LabelFrame(top_term, text="Current Term Entry Form")
    term_frame.grid(row=0, column=0, padx=20, pady=20)

    term_label = Label(term_frame, text="Enter current term: ")
    term_label.grid(row=0, column=0, padx=10, pady=10)

    term_entry_field = Entry(term_frame)
    term_entry_field.grid(row=0, column=1, padx=10, pady=10)

    term_label = Label(term_frame, text="Note: Term must be entered in the\n4 digit format (ie 2227, 2235, 2241, etc)")
    term_label.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

    term_submit_button = Button(term_frame, text="Submit", command=lambda: get_data())
    term_submit_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def get_data():
        schema = {'data': {'type': 'string', 'minlength': 4, 'maxlength': 4, 'regex': '^[0-9]+$' }}
        document =  {'data': term_entry_field.get()}
        v = Validator(schema)
        true_false = v.validate(document)

        if true_false == True:
            menu_gui.current_term_input(term_entry_field.get())
            top_term.destroy()
        if true_false == False:
            messagebox.showerror("Incorrect entry", "You must enter a 4 digit term. Try again.")
            

def close_and_leave():
    menu_gui.close_database()
    



# ---  GUI Development  ---
frame = Frame(root)
frame.pack()

current_term()

# Load data frame
load_frame = LabelFrame(frame, text="Load Files")
load_frame.grid(row=0, column=0, padx=20, pady=10)

load_all = Button(load_frame, text="*** Load All ***", command=lambda: verify_action("Load All Files?", menu_gui.load_all_files))
load_all.grid(row=0, column=0, columnspan=5, sticky="news")

load_contracts = Button(load_frame, text="Load Contracts Only", command=lambda: verify_action("Load Contract File?", menu_gui.load_contract_data))
load_contracts.grid(row=1, column=0)

load_ft_employee = Button(load_frame, text="Load FT Employee Only", command=lambda: verify_action("Load FT Employee File?", menu_gui.load_full_time_employee))
load_ft_employee.grid(row=1, column=1)

load_class_mode = Button(load_frame, text="Load Class Modes Only", command=lambda: verify_action("Load Class Mode File?", menu_gui.load_class_mode_data))
load_class_mode.grid(row=1, column=2)

load_benefit_eligible = Button(load_frame, text="Load Benefit Eligible Only", command=lambda: verify_action("Load Benefit Eligible File?", menu_gui.load_benefit_eligible_data))
load_benefit_eligible.grid(row=1, column=3)

load_jblm_type = Button(load_frame, text="Load JBLM Class Type Only", command=lambda: verify_action("Load JBLM Type File?", menu_gui.load_jblm_contract_type_data))
load_jblm_type.grid(row=1, column=4)

for widget in load_frame.winfo_children():
    widget.grid_configure(padx=10, pady=10)


# Stacking
stacking_frame = LabelFrame(frame, text="Stacking")
stacking_frame.grid(row=2, column=0, sticky="news", columnspan=4, padx=20, pady=10)

stacking_add_data = Button(stacking_frame, text="Add Stacking Data", command=stacking_add_data_func)
stacking_add_data.grid(row=0, column=0)

stacking_load_data = Button(stacking_frame, text="Load Stacking Data", command=lambda: verify_action("Load Stacking Data File?", menu_gui.load_stacked_data))
stacking_load_data.grid(row=0, column=1)

stacking_delete_data_combobox = ttk.Combobox(stacking_frame, values=['Single', 'All'])
stacking_delete_data_combobox.grid(row=1, column=2, padx=20, pady=20)
stacking_delete_data = Button(stacking_frame, text="Delete Stacking Data", command=lambda: stacking_delete_data_func(stacking_delete_data_combobox.get()))
stacking_delete_data.grid(row=0, column=2)

stacking_view_data = Button(stacking_frame, text="View Stacking Data", command=view_stacked)
stacking_view_data.grid(row=0, column=3)


for widget in stacking_frame.winfo_children():
    widget.grid_configure(padx=10, pady=10)


# Clear all data frame
clear_data_frame = LabelFrame(frame, text="Clear All Data")
clear_data_frame.grid(row=1, column=0, padx=20, pady=10, sticky='news')

clear_data_button = Button(clear_data_frame, text="Clear all table data", command=lambda: verify_action("*** WARNING ***\n\nThis will clear all data from all tables (except stacking) and is irreversible.\n\nStacking data will not be affected.\n\nContinue?", menu_gui.clear_all_data_tables))
clear_data_button.grid(row=0, column=0, sticky="news", padx=10, pady=10, columnspan=5)


# Perform analysis frame
perform_analysis_frame = LabelFrame(frame, text="Perform Analysis")
perform_analysis_frame.grid(row=3, column=0, sticky="news", columnspan=4, padx=20, pady=10)

perform_analysis_button = Button(perform_analysis_frame, text="Perform Analysis", command=lambda: verify_action_analysis("Has all data been updated for analysis?", menu_gui.perform_analysis)) 
perform_analysis_button.grid(row=0, column=0, sticky="news", padx=10, pady=10, columnspan=5)


# View data
view_data_frame = LabelFrame(frame, text="View Data")
view_data_frame.grid(row=4, column=0, sticky="news", columnspan=4, padx=20, pady=10)

view_contracts_combobox = ttk.Combobox(view_data_frame, values=['Single EMPL ID', 'All Records'])
view_contracts_combobox.grid(row=1, column=0, padx=20, pady=20)

view_contracts_button = Button(view_data_frame, text="View Contract Records", command=lambda: view_contract_records("View Contracts - All", view_contracts_combobox.get()))
view_contracts_button.grid(row=0, column=0, sticky="news", padx=10, pady=10)

view_results_combobox = ttk.Combobox(view_data_frame, values=['Single EMPL ID', 'All Records', 'Only Records to Review'])
view_results_combobox.grid(row=1, column=1, padx=20, pady=20)

view_results_button = Button(view_data_frame, text="View Final Results", command= lambda: view_final_results_records("Final Results", view_results_combobox.get()))
view_results_button.grid(row=0, column=1, padx=10, pady=10, sticky="news")


# Download Data
download_data_frame = LabelFrame(frame, text="Download Data")
download_data_frame.grid(row=5, column=0, sticky="news", columnspan=4, padx=20, pady=10)

download_stacked_button = Button(download_data_frame, text="Stacked Data", command=lambda: download_report("stacked"))
download_stacked_button.grid(row=0, column=0, sticky="news", padx=10, pady=10)

download_results_button = Button(download_data_frame, text="Final Results", command=lambda: download_report("final"))
download_results_button.grid(row=0, column=1, sticky="news", padx=10, pady=10)

# Exit frame
exit_frame = LabelFrame(frame, text="Exit Program")
exit_frame.grid(row=20, column=0, padx=20, pady=10, sticky="news")

exit_button = Button(exit_frame, text="Exit Program", command=close_and_leave)
exit_button.grid(row=20, column=0, padx=10, pady=10, columnspan=5)

mainloop()