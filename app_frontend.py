import tkinter as tk
from tkinter import messagebox
import flights_backend as fbe
import passengers_backend as pbe
import os

def clear_frame(root):
    for widget in root.winfo_children():
        widget.destroy()

class Starting_window:
    def __init__(self, master=None):
        # Constructor for the greeting window
        self.root = master
        self.root.title("Flight Database")
        window_width = self.root.winfo_screenwidth()
        window_height = self.root.winfo_screenheight()
        self.root.geometry(f"{window_width//4}x{window_height//3}")
        self.root.resizable(width=False, height=False)

        if not os.path.isfile("Databases/flights.db"):
            fbe.init_db()
        # if not os.path.isfile("Databases/passengers.db"):
        #     pbe.init_db()

        # Frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill='both', expand=True)

        title_frame = tk.Frame(main_frame, bg='gray')
        title_frame.columnconfigure(0, weight=1)
        title_frame.rowconfigure(0,weight=1)
        title_frame.pack(fill='both', expand=True, padx=5, pady=3)

        query_frame = tk.Frame(main_frame)
        query_frame.columnconfigure(0, weight=1)
        query_frame.columnconfigure(1, weight=1)
        query_frame.rowconfigure(0, weight=1)
        query_frame.rowconfigure(1, weight=2)
        query_frame.pack(fill='both', expand=True, padx=40, pady=10)

        action_frame = tk.Frame(main_frame)
        # action_frame.columnconfigure(0, weight=5)
        # action_frame.columnconfigure(1, weight=1)
        # action_frame.columnconfigure(2, weight=1)
        action_frame.pack(side='bottom', fill='x', padx=5, pady=3)

        # Labels
        self.lbl_title = tk.Label(title_frame, text="Flight Enquiry System", font='Arial 20 bold')
        self.lbl_title.grid(row=0, column=0, sticky='nwes', padx=5, pady=3)

        self.query_title = tk.Label(query_frame, text="What would you like to enquire about?", font='Arial 12')
        self.query_title.grid(row=0, columnspan=2, sticky='nsew')
        
        # Radiobutton to choose DB
        self.v = tk.StringVar(query_frame, 'None')
        self.rdiobtn_flight = tk.Radiobutton(query_frame, text="Flights", value='F', variable=self.v)
        self.rdiobtn_flight.grid(row=1, column=0, sticky='nsew')
        self.rdiobtn_passengers = tk.Radiobutton(query_frame, text="Passengers", value='P', variable=self.v)
        self.rdiobtn_passengers.grid(row=1, column=1, sticky='nsew')        

        # Buttons
        self.btn_exit = tk.Button(action_frame, text='Quit', font='Arial 12', command=self.on_closing)
        self.btn_exit.pack(side='right', fill='y')
        self.btn_done = tk.Button(action_frame, text='Next', font='Arial 12', command=self.on_done)
        self.btn_done.pack(side='right', fill='y')

        # Protocol
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        # Function handling the closing window
        if messagebox.askyesno(title="Quit?", message="Do you want to quit?"):
            self.root.destroy()

    def on_done(self):
        # Function handling actions after pressing done
        if self.v.get()=='None':
            messagebox.showinfo(title="Help", message="Choose one of the options!")
        elif self.v.get()=='F':
            clear_frame(self.root)
            flight_window = Flight_window(self)
        elif self.v.get()=='P':
            clear_frame(self.root)
            passenger_window = Passenger_window(self)

class Flight_window(Starting_window):
    def __init__(self, starting_window):
        self.root = starting_window.root
        self.root.title("Flights Enquiry Database")
        self.root.geometry("1260x720")

        FlightNo=tk.StringVar()
        Day=tk.StringVar()
        Month=tk.StringVar()
        Year=tk.StringVar()
        SchedDeptTime=tk.StringVar()
        SchedArrTime=tk.StringVar()
        Origin=tk.StringVar()
        Dest=tk.StringVar()
        Tailnum=tk.StringVar()
        CarrierShort=tk.StringVar()
        CarrierName=tk.StringVar()
        headers=['FlightNo', 'Date_Index', 'Scheduled_Dept_Time', 'Dept_Time', 'Scheduled_Arr_Time', 'Arr_Time', 'Air_Time', 'Origin', 'Destination', 'Tail No', 'Day', 'Month', 'Year', 'Carrier_Short', 'Carrier_Name']
        DataList = [FlightNo,Day,Month,Year,SchedDeptTime,SchedArrTime,Origin,Dest,Tailnum,CarrierShort,CarrierName]
        ColNameList = ['flightno', 'day', 'month', 'year', 'scheduled_dept_time', 'scheduled_arr_time', 'origin', 'dest', 'tailnum', "carrier_name", 'full_name']

        def viewflightdb():
            FlightList.delete(1, tk.END)
            for row in fbe.ViewAllData():
                FlightList.insert(tk.END, row)
        def searchflightdb():
            FlightList.delete(1, tk.END)
            SearchTerm = {}
            for Name, Data in zip(ColNameList, DataList):
                if Data.get()!='':
                    SearchTerm[Name] = Data.get()
            for row in fbe.SearchForData(SearchTerm):
                FlightList.insert(tk.END, row)
        
        def flightdatafill(event):
            global sd
            searchflight = FlightList.curselection()[0]
            sd = FlightList.get(searchflight)
            info_to_show = 'Data in Record:\n' + '\n'.join([a+": "+b for a, b in zip(headers, sd)])
            messagebox.showinfo(title="Selected Record", message=info_to_show)


        # Frames
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill='both', expand=True)

        title_frame = tk.Frame(main_frame)
        title_frame.columnconfigure(0, weight=1)
        title_frame.rowconfigure(0,weight=1)
        title_frame.pack(fill='x')

        data_frame = tk.Frame(main_frame, padx=5, pady=3)
        data_frame.columnconfigure(0, weight=2)
        data_frame.columnconfigure(1, weight=3)
        data_frame.rowconfigure(0, weight=1)
        data_frame.pack(fill='both', expand=True)
        data_frame_left = tk.Frame(data_frame,bg='green')
        data_frame_right = tk.Frame(data_frame,bg='red')
        data_frame_right.rowconfigure(0, weight=1)
        data_frame_right.columnconfigure(0, weight=1)
        data_frame_left.grid(row=0, column=0, sticky='nwes')
        data_frame_right.grid(row=0, column=1, sticky='nwes')

        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(fill='x', expand=True, side='bottom')

        # Labels and Entryboxes
        self.lblTitle = tk.Label(title_frame, text="Flight Enquiry System", font='Arial 20 bold')
        self.lblTitle.grid(row=0, column=0, sticky='nwes')

        self.lblFlightno = tk.Label(data_frame_left, text="Flight No: ", padx=5, pady=3)
        self.lblFlightno.grid(row=0, column=0, sticky='w')
        self.txtFlightno = tk.Entry(data_frame_left, textvariable=FlightNo, width=20)
        self.txtFlightno.grid(row=0, column=1)

        self.lblDay = tk.Label(data_frame_left, text="Day: ", padx=5, pady=3)
        self.lblDay.grid(row=1, column=0, sticky='w')
        self.txtDay = tk.Entry(data_frame_left, textvariable=Day, width=20)
        self.txtDay.grid(row=1, column=1)

        self.lblMonth = tk.Label(data_frame_left, text="Month: ", padx=5, pady=3)
        self.lblMonth.grid(row=2, column=0, sticky='w')
        self.txtMonth = tk.Entry(data_frame_left, textvariable=Month, width=20)
        self.txtMonth.grid(row=2, column=1)

        self.lblYear = tk.Label(data_frame_left, text="Year: ", padx=5, pady=3)
        self.lblYear.grid(row=3, column=0, sticky='w')
        self.txtYear = tk.Entry(data_frame_left, textvariable=Year, width=20)
        self.txtYear.grid(row=3, column=1)

        self.lblSchedDeptTime = tk.Label(data_frame_left, text="Scheduled Dept Time: ", padx=5, pady=3)
        self.lblSchedDeptTime.grid(row=4, column=0, sticky='w')
        self.txtSchedDeptTime = tk.Entry(data_frame_left, textvariable=SchedDeptTime, width=20)
        self.txtSchedDeptTime.grid(row=4, column=1)

        self.lblSchedArrTime = tk.Label(data_frame_left, text="Scheduled Arrival Time: ", padx=5, pady=3)
        self.lblSchedArrTime.grid(row=5, column=0, sticky='w')
        self.txtSchedArrTime = tk.Entry(data_frame_left, textvariable=SchedArrTime, width=20)
        self.txtSchedArrTime.grid(row=5, column=1)

        self.lblOrigin = tk.Label(data_frame_left, text="Origin: ", padx=5, pady=3)
        self.lblOrigin.grid(row=6, column=0, sticky='w')
        self.txtOrigin = tk.Entry(data_frame_left, textvariable=Origin, width=20)
        self.txtOrigin.grid(row=6, column=1)

        self.lblDest = tk.Label(data_frame_left, text="Destination: ", padx=5, pady=3)
        self.lblDest.grid(row=7, column=0, sticky='w')
        self.txtDest = tk.Entry(data_frame_left, textvariable=Dest, width=20)
        self.txtDest.grid(row=7, column=1)

        self.lblTailnum = tk.Label(data_frame_left, text="Tail Number: ", padx=5, pady=3)
        self.lblTailnum.grid(row=8, column=0, sticky='w')
        self.txtTailnum = tk.Entry(data_frame_left, textvariable=Tailnum, width=20)
        self.txtTailnum.grid(row=8, column=1)

        self.lblCarrierShort = tk.Label(data_frame_left, text="Carrier Shortform: ", padx=5, pady=3)
        self.lblCarrierShort.grid(row=9, column=0, sticky='w')
        self.txtCarrierShort = tk.Entry(data_frame_left, textvariable=CarrierShort, width=20)
        self.txtCarrierShort.grid(row=9, column=1)

        self.lblCarrierName = tk.Label(data_frame_left, text="Carrier Name: ", padx=5, pady=3)
        self.lblCarrierName.grid(row=10, column=0, sticky='w')
        self.txtCarrierName = tk.Entry(data_frame_left, textvariable=CarrierName, width=20)
        self.txtCarrierName.grid(row=10, column=1)

        sbVertical = tk.Scrollbar(data_frame_right, orient='vertical')
        sbVertical.grid(row=0, column=1, sticky='ns')
        sbHorizontal = tk.Scrollbar(data_frame_right, orient='horizontal')
        sbHorizontal.grid(row=1, column=0, sticky='we')

        FlightList = tk.Listbox(data_frame_right, font='Arial 12 bold', yscrollcommand=sbVertical.set, xscrollcommand=sbHorizontal.set)
        FlightList.bind("<<ListboxSelect>>", flightdatafill)
        FlightList.grid(row=0, column=0, sticky='nesw')
        sbVertical.config(command=FlightList.yview)
        sbHorizontal.config(command=FlightList.xview)
        FlightList.insert(tk.END, headers)

        # Buttons
        self.btnSearch = tk.Button(btn_frame, text="Search", command=searchflightdb)
        self.btnSearch.pack(side='right', padx=5, pady=3)
        self.btnDisplay = tk.Button(btn_frame, text='Display All', command=viewflightdb)
        self.btnDisplay.pack(side='right', padx=5, pady=3)


class Passenger_window(Starting_window):
    def __init__(self, starting_window):
        self.root = starting_window.root
        self.root.title("Passengers Enquiry Database")
        self.root.geometry("1260x720")


if __name__ == "__main__":
    root = tk.Tk()
    window = Starting_window(root)
    root.mainloop()

