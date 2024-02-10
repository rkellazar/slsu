import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import datetime
import matplotlib.pyplot as plt
from collections import Counter
import sqlite3
from datetime import datetime, date


DB_PATH = "database/turnstile.db"
stu_dict_in_val, stu_dict_out_val, tea_dict_in_val, tea_dict_out_val, non_dict_in_val, non_dict_out_val, max_val = {}, {}, {}, {}, {}, {}, 0


def load_data():
    path = DB_PATH
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    query = """
        SELECT ts.id, ts.category, ts.first_name, ts.initial_name, ts.last_name, ts.course, ts.department, ts.phone_number, tl.login_time, tl.inout
        FROM TimelogData as tl
        LEFT JOIN TurnstileData as ts ON ts.id = tl.id
        ORDER BY tl.login_time;
    """

    cursor.execute(query)
    results = cursor.fetchall()

    conn.close()

    stu_in_val = []
    stu_out_val = []
    non_in_val = []
    non_out_val = []
    tea_in_val = []
    tea_out_val = []

    columns = ['ID', 'Role', 'First Name', 'M.I.', 'Last Name', 'College', 'Department', 'Phone Number', 'Time Log', 'In/Out']

    for col_name in columns:
        treeview.heading(col_name, text=col_name)

    for value_tuple in results:
        datetime_object = datetime.strptime(value_tuple[8], '%Y-%m-%d %H:%M:%S')
        treeview.insert('', tk.END, values=value_tuple)

        if value_tuple[9] == "IN" and value_tuple[1] == "Student":
            stu_in_val.append(datetime_object.hour)
        elif value_tuple[9] == "OUT" and value_tuple[1] == "Student":
            stu_out_val.append(datetime_object.hour)

        if value_tuple[9] == "IN" and value_tuple[1] == "Teaching Personnel":
            tea_in_val.append(datetime_object.hour)
        elif value_tuple[9] == "OUT" and value_tuple[1] == "Teaching Personnel":
            tea_out_val.append(datetime_object.hour)

        if value_tuple[9] == "IN" and value_tuple[1] == "Non-Teaching Personnel":
            non_in_val.append(datetime_object.hour)
        elif value_tuple[9] == "OUT" and value_tuple[1] == "Non-Teaching Personnel":
            non_out_val.append(datetime_object.hour)

    global stu_dict_in_val, stu_dict_out_val, tea_dict_in_val, tea_dict_out_val, non_dict_in_val, non_dict_out_val, max_val
    stu_dict_in_val, stu_dict_out_val, tea_dict_in_val, tea_dict_out_val, non_dict_in_val, non_dict_out_val, max_val = chart_value(
        stu_in_val, stu_out_val, tea_in_val, tea_out_val, non_in_val, non_out_val)

       
def filter_data():
    stu_in_val = []
    stu_out_val = []
    non_in_val = []
    non_out_val = []
    tea_in_val = []
    tea_out_val = []

    # Clear existing items in the treeview
    treeview.delete(*treeview.get_children())

    # Get filter values from user input
    filter_id = id_entry.get() if id_entry.get() != "ID" else ""
    filter_inout = status_inout.get()
    filter_role = status_combobox.get()

    filter_from_month = start_month_entry.get() if start_month_entry.get().isdigit() else "1"
    filter_from_day = start_day_entry.get() if start_day_entry.get().isdigit() else "1"
    filter_from_year = start_year_entry.get() if start_year_entry.get().isdigit() else "1900"

    filter_to_month = end_month_entry.get() if end_month_entry.get().isdigit() else "12"
    filter_to_day = end_day_entry.get() if end_day_entry.get().isdigit() else "31"
    filter_to_year = end_year_entry.get() if end_year_entry.get().isdigit() else f"{datetime.today().year}"

    path = DB_PATH
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    query = """
        SELECT ts.id, ts.category, ts.first_name, ts.initial_name, ts.last_name, ts.course, ts.department, ts.phone_number, tl.login_time, tl.inout
        FROM TimelogData as tl
        LEFT JOIN TurnstileData as ts ON ts.id = tl.id
        ORDER BY tl.login_time;
    """

    cursor.execute(query)
    results = cursor.fetchall()

    conn.close()

    print(f"From Date: {filter_from_year}, {filter_from_month}, {filter_from_day}")
    print(f"To Date: {filter_to_year}, {filter_to_month}, {filter_to_day}")

    for row in results:
        date_in_row = datetime.strptime(row[8], '%Y-%m-%d %H:%M:%S')

        if ((filter_id == row[0] or not filter_id) and
                (filter_inout == row[9] or filter_inout == "[ALL IN/OUT]") and
                (filter_role == row[1] or filter_role == "[ALL ROLES]")):

            from_date = date(int(filter_from_year), int(filter_from_month), int(filter_from_day))
            to_date = date(int(filter_to_year), int(filter_to_month), int(filter_to_day))

            if not filter_from_month or date_in_row.date() >= from_date:
                if not filter_to_month or date_in_row.date() <= to_date:
                    treeview.insert('', tk.END, values=row)

                    if row[9] == "IN" and row[1] == "Student":
                        stu_in_val.append(date_in_row.hour)
                    elif row[9] == "OUT" and row[1] == "Student":
                        stu_out_val.append(date_in_row.hour)

                    if row[9] == "IN" and row[1] == "Teaching Personnel":
                        tea_in_val.append(date_in_row.hour)
                    elif row[9] == "OUT" and row[1] == "Teaching Personnel":
                        tea_out_val.append(date_in_row.hour)

                    if row[9] == "IN" and row[1] == "Non-Teaching Personnel":
                        non_in_val.append(date_in_row.hour)
                    elif row[9] == "OUT" and row[1] == "Non-Teaching Personnel":
                        non_out_val.append(date_in_row.hour)

    stu_dict_in_val, stu_dict_out_val, tea_dict_in_val, tea_dict_out_val, non_dict_in_val, non_dict_out_val, max_val = chart_value(
        stu_in_val, stu_out_val, tea_in_val, tea_out_val, non_in_val, non_out_val)

    global one_fig, one_ax, two_fig, two_ax, three_fig, three_ax
    update_chart(one_fig, one_ax, stu_dict_in_val, stu_dict_out_val, "Student", max_val)
    update_chart(two_fig, two_ax, tea_dict_in_val, tea_dict_out_val, "Teaching Personnel", max_val)
    update_chart(three_fig, three_ax, non_dict_in_val, non_dict_out_val, "Non-Teaching Personnel", max_val)


def chart_value(stu_in_val, stu_out_val, tea_in_val, tea_out_val, non_in_val, non_out_val):
    stu_dict_in_val = {key: 0 for key in range(24)}
    stu_dict_out_val = {key: 0 for key in range(24)}
    tea_dict_in_val = {key: 0 for key in range(24)}
    tea_dict_out_val = {key: 0 for key in range(24)}
    non_dict_in_val = {key: 0 for key in range(24)}
    non_dict_out_val = {key: 0 for key in range(24)}

    # Count occurrences of each element
    stu_count_in = Counter(stu_in_val)
    stu_count_out = Counter(stu_out_val)
    tea_count_in = Counter(tea_in_val)
    tea_count_out = Counter(tea_out_val)
    non_count_in = Counter(non_in_val)
    non_count_out = Counter(non_out_val)

    # Calculate average for each unique element
    stu_in_averages = {key: key / count for key, count in stu_count_in.items()}
    stu_out_averages = {key: key / count for key, count in stu_count_out.items()}
    tea_in_averages = {key: key / count for key, count in tea_count_in.items()}
    tea_out_averages = {key: key / count for key, count in tea_count_out.items()}
    non_in_averages = {key: key / count for key, count in non_count_in.items()}
    non_out_averages = {key: key / count for key, count in non_count_out.items()}

    for key, average in stu_in_averages.items():
        stu_dict_in_val[key] = average

    for key, average in stu_out_averages.items():
        stu_dict_out_val[key] = average

    for key, average in tea_in_averages.items():
        tea_dict_in_val[key] = average

    for key, average in tea_out_averages.items():
        tea_dict_out_val[key] = average

    for key, average in non_in_averages.items():
        non_dict_in_val[key] = average

    for key, average in non_out_averages.items():
        non_dict_out_val[key] = average

    max_val = max(list(stu_dict_in_val.values()) + list(stu_dict_out_val.values()) + list(tea_dict_in_val.values()) +
                list(tea_dict_out_val.values()) + list(non_dict_in_val.values()) + list(non_dict_out_val.values()))


    return stu_dict_in_val, stu_dict_out_val, tea_dict_in_val, tea_dict_out_val, non_dict_in_val, non_dict_out_val, max_val


def create_chart(line1, line2, col_num, title, max_val):
    chart_frame = ttk.LabelFrame(analysis_tab)
    chart_frame.grid(row=1, column=col_num, padx=20, pady=10, sticky="W")

    fig, ax = plt.subplots(figsize=(1.75, 1.6), dpi=100)

    x_values = np.arange(0, 24)
    y_values_line1 = list(line1.values())
    y_values_line2 = list(line2.values())

    ax.plot(x_values, y_values_line1, label='Line 1', color='blue', linewidth=0.5)
    ax.plot(x_values, y_values_line2, label='Line 2', color='orange', linewidth=0.5)

    for spine in ax.spines.values():
        spine.set_linewidth(0.5)

    ax.set_title(title, fontsize=5)
    ax.tick_params(axis='both', which='major', labelsize=5, size=2) 

    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=col_num, column=0, pady=10, padx=20)

    ax.set_ylim(bottom=0, top=max_val+1)

    canvas.draw()

    return fig, ax
    

def update_chart(fig, ax, new_line1, new_line2, title, new_max_val):
    x_values = np.arange(0, 24)
    y_values_line1 = list(new_line1.values())
    y_values_line2 = list(new_line2.values())

    ax.clear()
    ax.plot(x_values, y_values_line1, label='Line 1', color='blue', linewidth=0.5)
    ax.plot(x_values, y_values_line2, label='Line 2', color='orange', linewidth=0.5)

    ax.tick_params(axis='both', which='major', labelsize=5) 

    ax.set_title(title, fontsize=5)
    ax.set_ylim(bottom=0, top=new_max_val + 1)

    fig.canvas.draw_idle()


def set_placeholder(entry, placeholder_text):
    entry.insert(0, placeholder_text)
    entry.bind("<FocusIn>", lambda e: on_entry_click(entry, placeholder_text))
    entry.bind("<FocusOut>", lambda e: on_focus_out(entry, placeholder_text))

def on_entry_click(entry, placeholder_text):
    if entry.get() == placeholder_text:
        entry.delete(0, "end")
        entry.config(foreground="black")

def on_focus_out(entry, placeholder_text):
    if entry.get() == "":
        entry.insert(0, placeholder_text)
        entry.config(foreground="grey")


root = tk.Tk()
root.title("SLSU Timelog")

style = ttk.Style(root)
root.tk.call("source", "forest-light.tcl")
style.theme_use("forest-light")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# ----- Time Log Tab -----

frame = ttk.Frame(notebook)
notebook.add(frame, text="Timelog Data")

widgets_frame = ttk.LabelFrame(frame, text="Filter Data")
widgets_frame.grid(row=0, column=0, padx=20, pady=10, sticky="N")

id_entry = ttk.Entry(widgets_frame)
set_placeholder(id_entry, "ID")
id_entry.grid(row=0, column=0, padx=5, pady=(10, 15), sticky="EW")

inout_list = ["[ALL IN/OUT]", "IN", "OUT"]

status_inout = ttk.Combobox(widgets_frame, values=inout_list)
status_inout.current(0)
status_inout.grid(row=1, column=0, padx=5, pady=(0, 15), sticky="EW")

combo_list = ["[ALL ROLES]", "Student", "Teaching Personnel", "Non-Teaching Personnel"]

status_combobox = ttk.Combobox(widgets_frame, values=combo_list)
status_combobox.current(0)
status_combobox.grid(row=2, column=0, padx=5, pady=(0, 15), sticky="EW")

from_date_frame = ttk.LabelFrame(widgets_frame, text="From")
from_date_frame.grid(row=3, column=0, padx=5, pady=(0, 5), sticky="EW")

start_month_entry = ttk.Entry(from_date_frame, width=4)
set_placeholder(start_month_entry, "MM")
start_month_entry.grid(row=0, column=0, padx=5, pady=(0, 5), sticky="EW")

start_day_entry = ttk.Entry(from_date_frame, width=4)
set_placeholder(start_day_entry, "DD")
start_day_entry.grid(row=0, column=1, padx=5, pady=(0, 5), sticky="EW")

start_year_entry = ttk.Entry(from_date_frame, width=6)
set_placeholder(start_year_entry, "YYYY")
start_year_entry.grid(row=0, column=2, padx=5, pady=(0, 5), sticky="EW")

to_date_frame = ttk.LabelFrame(widgets_frame, text="To")
to_date_frame.grid(row=4, column=0, padx=5, pady=(0, 5), sticky="EW")

end_month_entry = ttk.Entry(to_date_frame, width=4)
set_placeholder(end_month_entry, "MM")
end_month_entry.grid(row=0, column=0, padx=5, pady=(0, 5), sticky="EW")

end_day_entry = ttk.Entry(to_date_frame, width=4)
set_placeholder(end_day_entry, "DD")
end_day_entry.grid(row=0, column=1, padx=5, pady=(0, 5), sticky="EW")

end_year_entry = ttk.Entry(to_date_frame, width=6)
set_placeholder(end_year_entry, "YYYY")
end_year_entry.grid(row=0, column=2, padx=5, pady=(0, 5), sticky="EW")

separator = ttk.Separator(widgets_frame)
separator.grid(row=5, column=0, padx=(20, 20), pady=10, sticky="EW")

button = ttk.Button(widgets_frame, text="Filter", command=filter_data)
button.grid(row=6, column=0, padx=5, pady=(0, 15), sticky="NSEW")

treefFrame = ttk.Frame(frame)
treefFrame.grid(row=0, column=1, pady=10)
treeScroll = ttk.Scrollbar(treefFrame)
treeScroll.pack(side="right", fill="y")

cols = ("ID", "Role", "First Name", "M.I.", "Last Name", "College", "Department", "Phone Number", "Time Log", "In/Out")
treeview = ttk.Treeview(treefFrame, show="headings", columns=cols, height=20, yscrollcommand=treeScroll.set, selectmode="browse")

treeview.column("ID", width=100)
treeview.column("Role", width=140)
treeview.column("First Name", width=100)
treeview.column("M.I.", width=50)
treeview.column("Last Name", width=100)
treeview.column("College", width=100)
treeview.column("Department", width=80)
treeview.column("Phone Number", width=100)
treeview.column("Time Log", width=150)
treeview.column("In/Out", width=50)

treeview.pack()
treeScroll.config(command=treeview.yview)

load_data()

# ----- Data Analysis Tab -----

analysis_tab = ttk.Frame(notebook)
notebook.add(analysis_tab, text="Data Analysis")

analysis_title = ttk.Label(analysis_tab, text="Hourly Averages: Insights into Tap Trends", font=('TkDefaultFont', 20))
analysis_title.grid(row=0, column=1, padx=20, pady=10, sticky="NW")

one_fig, one_ax = create_chart(stu_dict_in_val, stu_dict_out_val, 0, "STUDENT", max_val)
two_fig, two_ax = create_chart(tea_dict_in_val, tea_dict_out_val, 1, "TEACHING PERSONNEL", max_val)
three_fig, three_ax = create_chart(non_dict_in_val, non_dict_out_val, 3, "NON-TEACHING PERSONNEL", max_val)

legend_label1 = ttk.Label(analysis_tab, text="—— IN", foreground="blue")
legend_label1.grid(row=2, column=1, padx=20, pady=(10, 0), sticky="S")

legend_label2 = ttk.Label(analysis_tab, text="—— OUT", foreground="orange")
legend_label2.grid(row=3, column=1, padx=20, pady=0, sticky="S")

root.mainloop()
