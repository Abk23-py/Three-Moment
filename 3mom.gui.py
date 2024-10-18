import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import *
import three_Moment as tm
from indeterminatebeam import Beam, PointLoadV, DistributedLoadV
from indeterminatebeam import Support as Sp
import plotly 
import plotly.io as io
io.renderers.default = 'browser'

beam = tk.Tk()
beam.title('3 Moment Master(3MM)')
beam.geometry('1366x768')
beam.resizable(True, True)

mainFrame = tk.Frame(beam)
mainFrame.pack(fill="both", expand=1)

def FrameWidth(event):
    canvasWidth = event.width
    canvas.itemconfig(canvasFrame, width=canvasWidth)


def OnFrameConfigure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))


# Creating a Canvas for the widgets and all items in the gui
canvas = tk.Canvas(mainFrame, bg="blue")
canvas.pack(side="left", fill="both", expand=1)

# Adding a Scrollbar To the Canvas
my_scrollbar = ttk.Scrollbar(mainFrame, orient="vertical", command=canvas.yview)
my_scrollbar.pack(side="right", fill="y")


canvas.configure(yscrollcommand=my_scrollbar.set)

canvas.bind('<Configure>', FrameWidth)
# Creating Another Frame INSIDE the Canvas
second_frame = tk.Frame(canvas, bg="blue")
second_frame.pack(fill="both", expand=1)

second_frame.bind("<Configure>", OnFrameConfigure)
# Adding that new frame to a Window In the Canvas
canvasFrame = canvas.create_window((0, 0), window=second_frame, anchor="nw" )


container = ttk.LabelFrame(second_frame, text='Beam Data')
container.grid(row=0, column=0, columnspan=3)

node_label = ttk.Label(container, text='Number of Nodes',background='red')
node_label.grid(row=0, column=0, padx=5, pady=10,sticky=tk.W)


num_nodes = tk.StringVar()
node_entry = ttk.Entry(container, width=10, textvariable=num_nodes,foreground='green')
node_entry.grid(row=0, column=1, padx=5, pady=5)

#  Defining containers and global variables
list_PL = []
list_UDL = []
list_SPANS = []
list_3_Moment = []


def NodeProceed():
    global node_list, nodes
    global list_of_node_names

    nodes = int(num_nodes.get())
    node_list = [0] * nodes
    list_of_node_names = []
    for i in range(nodes):
        node = 'Node ' + str(i+1)
        list_of_node_names.append(node)

    comboNodeselected = tk.StringVar()
    combo_box =ttk.Combobox(second_frame, textvariable=comboNodeselected)
    combo_box.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
    combo_box['values'] = list_of_node_names
    
    def ComboNodeSelected(event):
        nodeXentered = tk.StringVar()
        nodeYentered = tk.StringVar()
        node_info_frame = ttk.LabelFrame(second_frame, text=comboNodeselected.get() + ' Information')
        node_info_frame.grid(row=2, column=0, sticky=tk.W)
        x_label = ttk.Label(node_info_frame, text='x_value',foreground='black',background='blue',font='bold')
        x_label.grid(row=0, column=0, padx=10, pady=10)
        x_entry = ttk.Entry(node_info_frame, textvariable=nodeXentered,foreground='red')
        x_entry.grid(row=0, column=1, padx=10, pady=10)

        y_label = ttk.Label(node_info_frame, text='y_value',foreground='black',background='blue',font='bold')
        y_label.grid(row=1, column=0, padx=10, pady=10)
        y_entry = ttk.Entry(node_info_frame, textvariable=nodeYentered,foreground='red')
        y_entry.grid(row=1, column=1, padx=10, pady=10)
        y_entry.insert(0, 0)
        
        def save_node():
            nodeN =comboNodeselected.get()
            nodeN = nodeN.split(' ')
            nodeN = int(nodeN[1])
            node_index = int(nodeN-1)
            node_list[node_index] = tm.Node(float(nodeXentered.get()), float(nodeYentered.get()))
            # Node_list.append(tm.Node(float(nodeXentered.get()), float(nodeYentered.get())))
            messagebox.showinfo('Node Save prompt', comboNodeselected.get() + ' properties have been saved successfully')
        save_button = ttk.Button(node_info_frame, text='Save', command=save_node)
        save_button.grid(row=2, column=1, sticky=tk.E, padx=10, pady=10)


    combo_box.bind('<<ComboboxSelected>>', ComboNodeSelected)


node_button = ttk.Button(container, width=15, text='Node Proceed', command=NodeProceed)
node_button.grid(row=0, column=2, padx=5, pady=10)


support_label = ttk.Label(container, text='Number of Supports',background='red')
support_label.grid(row=1, column=0, padx=5, pady=10,sticky=tk.W)

num_supports = tk.StringVar()

support_entry = ttk.Entry(container, width=10, textvariable=num_supports,foreground='green')
support_entry.grid(row=1, column=1, padx=5, pady=10)


def SupportProceed():
    global listOfSupports
    global supports
    global list_of_support_names
    supports = int(num_supports.get())
    list_of_support_names = []
    listOfSupports = [0]*supports
    for i in range(supports):
        support  = 'Support ' + str(i+1)
        list_of_support_names.append(support)
    supportSeleceted = tk.StringVar()
    combobox_support = ttk.Combobox(second_frame, textvariable=supportSeleceted,background='yellow')
    combobox_support.grid(row=1, column=1, sticky=tk.W)
    combobox_support['values'] = list_of_support_names
    
    def ComboSupportSelected(event):
        
        support_info_frame = ttk.LabelFrame(second_frame, text=supportSeleceted.get() + ' Information')
        support_info_frame.grid(row=2, column=1, sticky=tk.W)
        ttk.Label(support_info_frame, text='Support Node Name',foreground='green').grid(row=0, column=0, padx=10, pady=10)
        sNode=tk.StringVar()
        S_Node = ttk.Combobox(support_info_frame, textvariable=sNode,foreground='red')
        S_Node.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)
        S_Node['values'] = list_of_node_names
        
        S_Type=tk.StringVar()
        ttk.Label(support_info_frame, text='Support Type',foreground='green').grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        S_Type_combo = ttk.Combobox(support_info_frame,textvariable=S_Type,foreground='red')
        S_Type_combo.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)
        S_Type_combo['values']=["pin", "roller", "fixed"]
        
        def save_support():
            supporti = supportSeleceted.get()
            supporti = supporti.split(" ")
            supporti = int(supporti[1])
            supporti_ind = int(supporti-1)
            
            supportN=sNode.get()
            supportN=supportN.split(" ")
            supportN=int(supportN[1])
            supportN_ind = int(supportN-1)
            supportNode=node_list[supportN_ind]
            
            listOfSupports[supporti_ind] = tm.Support(supportNode, S_Type.get())
            tk.messagebox.showinfo('Support Save prompt', supportSeleceted.get() +' properties have been saved successfully')
            
                       
        saveSupport = ttk.Button(support_info_frame, text='Save',command=save_support)
        saveSupport.grid(row=2, column=1, sticky=tk.E, padx=10, pady=10)
        

    combobox_support.bind("<<ComboboxSelected>>",ComboSupportSelected)


support_button = ttk.Button(container, width=15,text='Support Proceed', command=SupportProceed)
support_button.grid(row=1, column=2, padx=5, pady=10)

load_label = ttk.Label(container, text='Number of Loads',background='red')
load_label.grid(row=2, column=0, padx=5, pady=10,sticky=tk.W)

num_loads = tk.StringVar()
load_entry = ttk.Entry(container, width=10, textvariable=num_loads)
load_entry.grid(row=2, column=1, padx=5, pady=10)


def LoadProceed():
    global listOfLoads
    global loads
    loads = int(num_loads.get())
    list_of_load_names = []
    listOfLoads = [0] * loads
    for i in range(loads):
        load = 'Load ' + str(i+1)
        list_of_load_names.append(load)
    loadSeleceted = tk.StringVar()
    combobox_load = ttk.Combobox(second_frame, textvariable=loadSeleceted,foreground='red',background='green')
    combobox_load.grid(row=1, column=3, sticky=tk.W)
    combobox_load['values'] = list_of_load_names

    def ComboLoadSelected(event):
        load_info_frame = ttk.LabelFrame(second_frame, text='Load Type Information')
        load_info_frame.grid(row=2, column=3, sticky=tk.W)


        L_Type = tk.StringVar()
        ttk.Label(load_info_frame, text='Load Type').grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        L_Type_combo = ttk.Combobox(load_info_frame, textvariable=L_Type)
        L_Type_combo.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)
        L_Type_combo['values'] = ["Point Load", "UDL"]

        def ComboLTypeSelected(event):
            pl_type_frame = ttk.LabelFrame(second_frame, text=loadSeleceted.get() + ' Information - Point Load')
            pl_type_frame.grid(row=2, column=3, sticky=tk.W)

            udl_type_frame = ttk.LabelFrame(second_frame, text=loadSeleceted.get() + ' Information - UDL')
            udl_type_frame.grid(row=2, column=4, sticky=tk.W)

            magnitude = tk.StringVar()  # magnitude of the load
            intensity = tk.StringVar()   # intensity of the UDL

            if event.widget.get() == "Point Load":
                pNode = tk.StringVar()
                ttk.Label(pl_type_frame, text='Load Node Name').grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
                L_Node = ttk.Combobox(pl_type_frame, textvariable=pNode)
                L_Node.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)
                L_Node['values'] = list_of_node_names

                ttk.Label(pl_type_frame, text='Magnitude(kN)').grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
                mag_entry = ttk.Entry(pl_type_frame, textvariable=magnitude, width=6)
                mag_entry.grid(row=1, column=1, pady=10, padx=10, sticky=tk.W)

                def save_pl():
                    listOfPL = []
                    loadi = loadSeleceted.get()
                    loadi = loadi.split(" ")
                    loadi = int(loadi[1])
                    loadi_ind = int(loadi - 1)

                    loadN = pNode.get()
                    loadN = loadN.split(" ")
                    loadN = int(loadN[1])
                    loadN_ind = int(loadN - 1)
                    loadNode = node_list[loadN_ind]

                    listOfLoads[loadi_ind] = tm.PointLoad(loadNode, float(magnitude.get()))
                    messagebox.showinfo('Load Save prompt',loadSeleceted.get() +  'properties saved')

                savePL = ttk.Button(pl_type_frame, text='Save', command=save_pl)
                savePL.grid(row=2, column=3, sticky=tk.E, padx=10, pady=10)


            elif event.widget.get() == "UDL":
                sSupport = tk.StringVar()
                eSupport = tk.StringVar()
                ttk.Label(udl_type_frame, text='start Support').grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
                start_Support = ttk.Combobox(udl_type_frame, textvariable=sSupport)
                start_Support.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)
                start_Support['values'] = list_of_support_names

                ttk.Label(udl_type_frame, text='end Support').grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
                end_Support = ttk.Combobox(udl_type_frame, textvariable=eSupport)
                end_Support.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)
                end_Support['values']  = list_of_support_names

                ttk.Label(udl_type_frame, text='intensity(kN/m)').grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
                mag_entry = ttk.Entry(udl_type_frame, textvariable=intensity, width=6)
                mag_entry.grid(row=2, column=1, pady=10, padx=10, sticky=tk.W)

                def save_udl():
                    listOfUDL = []
                    loadi = loadSeleceted.get()
                    loadi = loadi.split(" ")
                    loadi = int(loadi[1])
                    loadi_ind = int(loadi - 1)

                    startUdl = sSupport.get()
                    endUdl = eSupport.get()
                    startN = int(startUdl.split(" ")[1])
                    endN = int(endUdl.split(" ")[1])
                    startN_ind = startN - 1
                    endN_ind = endN - 1
                    startSupport = listOfSupports[startN_ind]
                    endSupport = listOfSupports[endN_ind]

                    listOfLoads[loadi_ind] = tm.UDL(startSupport,endSupport, float(intensity.get()))
                    messagebox.showinfo('Save', 'UDL properties saved')

                saveUDL = ttk.Button(udl_type_frame, text='Save', command=save_udl)
                saveUDL.grid(row=3, column=3, sticky=tk.E, padx=10, pady=10)


        L_Type_combo.bind("<<ComboboxSelected>>", ComboLTypeSelected)
    combobox_load.bind("<<ComboboxSelected>>", ComboLoadSelected)

load_button = ttk.Button(container, width=15,text='Load Proceed', command=LoadProceed)
load_button.grid(row=2, column=2, padx=5, pady=10)

def close_window():
    beam.destroy()

solve_butt = ttk.Button(second_frame, text='Solve', command=close_window)
solve_butt.grid(row=0, column=3, padx=20, pady=20)

beam.mainloop()



#  Getting the lsit of PL and UDL for our Solver
for load in listOfLoads:
    if load.__class__.__name__ == 'UDL' :
        list_UDL.append(load)
    else:
        list_PL.append(load)

for i in range(len(listOfSupports) - 1):
    pl_LIST = []
    udl_LIST =[]
    leftSupport = listOfSupports[i]
    rightSupport = listOfSupports[i + 1]

    for pl in list_PL:#
        if leftSupport.node.x < pl.node.x < rightSupport.node.x :
            pl_LIST.append(pl)

    for udl in list_UDL :
        if (udl.startSupport.node.x == leftSupport.node.x) and (udl.endSupport.node.x == rightSupport.node.x):
            udl_LIST.append(udl)
    span = tm.Span(leftSupport, rightSupport, pl_LIST, udl_LIST)
    list_SPANS.append(span)

for i in range(len(list_SPANS) - 1):
    leftspan = list_SPANS[i]
    rightspan = list_SPANS[i+1]
    list_3_Moment.append(tm.TMSpan(leftspan, rightspan))

solve = tm.QsSolver(node_list, listOfSupports, list_PL, list_UDL, list_3_Moment, list_SPANS)

Moments, Reactions = solve.calculate()


win2 = tk.Tk()
win2.title('Results of Three Moment')
win2.resizable(True, True)


resultsFrame = ttk.LabelFrame(win2, text='Moments')
resultsFrame.grid(row=0, column=1)
reactionsFrame = ttk.LabelFrame(win2, text='Reactions at Supports Within each span(in kN)')
reactionsFrame.grid(row=2, column=3)

def solve():

    for i in range(len(Moments)):
        ttk.Label(resultsFrame, text=f'\nMoment {i+1} \t = \t  {round(Moments[i], 2)} kNm\n').grid(row=i+2, sticky=tk.W)

    ttk.Label(reactionsFrame, text='Span Number\t\tLeft Reaction\t\tRight Reaction').grid(row=0, column=0, columnspan=3, sticky=tk.W)
    for i in range(len(Reactions)):
        ttk.Label(reactionsFrame, text=f'\t{i+1}\t\t\t{round(Reactions[i][0], 2)}\t\t\t{round(Reactions[i][1], 2)}').grid(row=i+2, column=0,
                                                                                                                    columnspan=3,sticky=tk.W )


ResultsButton = ttk.Button(win2, text='Calculate', command=solve)
ResultsButton.grid(row=0, column=0, padx=10, pady=10)


win2.mainloop()

beam_length = 0
for span in list_SPANS:
    beam_length += span.length()

beam = Beam(beam_length)
supps = []
loads = []

for s in listOfSupports:
    x = s.node.x
    supp = Sp(x, (1, 1, 0))
    supps.append(supp)

for pl in list_PL:
    mag = pl.magnitude
    xp = pl.node.x
    load = PointLoadV(mag*1000, xp)
    loads.append(load)

for udl in list_UDL:
    w = udl.intensity
    startx = udl.startSupport.node.x
    endx = udl.endSupport.node.x
    load = DistributedLoadV(w*1000, (startx, endx))
    loads.append(load)

beam.add_supports(*supps)
beam.add_loads(*loads)

beam.analyse()
fig_1 = beam.plot_beam_external()
fig_1.show()

fig_2 = beam.plot_beam_internal()
fig_2.show()
