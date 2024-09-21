import tkinter as tk
from tkinter import *
from tkinter import messagebox
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')
ctk.deactivate_automatic_dpi_awareness()
ctk.set_window_scaling(1)
ctk.set_widget_scaling(1)

class Compound_Interest_GUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        # Set up root window
        self.title("Interest Calculator")
        self.geometry('400x520')
        self.resizable(False, False)
        self.grid_columnconfigure((0,3), weight = 1)
        self.grid_rowconfigure((0,8), weight = 1)

        """
        Create Tabview and Tabs
        """
        # create tabview
        self.my_tab = ctk.CTkTabview(self,
                        width = 950,
                        height = 500, 
                        corner_radius= 1,
                        fg_color='black',
                        segmented_button_fg_color= 'dark green',
                        segmented_button_selected_color='green',
                        text_color='silver',
                        anchor = 'nw'
                        )
        self.my_tab.propagate(0)
        self.my_tab.pack(padx = 10, pady = 10)

        # create tabs
        self.tab_1 = self.my_tab.add('Compound Interest')
        self.tab_2 = self.my_tab.add('Simple Interest')

        """
        Set up main investment contribution frame
        """

        self.main_contribution = ctk.CTkFrame(self.tab_1, corner_radius=10,
                                              fg_color='black',
                                              height=300, width = 400
                                              )
        self.main_contribution.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = 'nw')

        # Set up label and entry box for user's initial investment
        self.initial_investment_header = ctk.CTkLabel(self.main_contribution, 
                                                      text = 'Initial Investment: ',
                                                      font = ('Arial', 12))
        self.initial_investment_header.grid(row = 0, column = 0, padx = 10, pady = (10,0), sticky = 'w')

        self.initial_investment = ctk.CTkEntry(self.main_contribution, placeholder_text= 'Enter the initial investment amount: ',
                                               placeholder_text_color = 'light grey',
                                               font = ('Arial', 12),
                                               width = 220)
        self.initial_investment.grid(row = 1, column = 0, padx = 10, pady = (10,0), sticky = 'ew')

        # Set up label and entry box for user's interest rate
        self.initial_rate_header = ctk.CTkLabel(self.main_contribution, 
                                                text = 'Interest Rate: ',
                                                font = ('Arial', 12))
        self.initial_rate_header.grid(row = 2, column = 0, padx = 10, pady = (10,0), sticky = 'w')

        self.interest_rate = ctk.CTkEntry(self.main_contribution, placeholder_text = 'Enter the interest rate percentage: ',
                                        placeholder_text_color= 'light grey',
                                        font = ('Arial', 12),
                                        width = 220)
        self.interest_rate.grid(row = 3, column = 0, padx = 10, pady = (10,0), sticky = 'ew')

        # Set up combobox so user can choose the interest rate type
        self.interest_rate_options = ['daily', 'monthly', 'quarterly', 'yearly']
        self.interest_rate_combobox = ctk.CTkComboBox(self.main_contribution, font = ('Arial', 12),
                                            corner_radius= 1, width = 90,
                                            values = self.interest_rate_options)
        self.interest_rate_combobox.grid(row = 3, column = 1, padx = 10, pady = (10,0), sticky = 'w')
        self.interest_rate_combobox.set('monthly')
        
        # Set up entry box for length of investment period
        self.investment_period_header = ctk.CTkLabel(self.main_contribution, 
                                                     text = 'Investment Length: ',
                                                     font = ('Arial', 12))
        self.investment_period_header.grid(row = 4, column = 0, padx = 10, pady = (10,0), sticky = 'w')

        # Set up years
        self.investment_years = ctk.CTkLabel(self.main_contribution, text = 'Years:', 
                                              font = ('Arial', 12))
        self.investment_years.grid(row = 5, column = 0, padx = 10, pady = 5, sticky = 'w')

        self.investment_period_years = ctk.CTkEntry(self.main_contribution,
                                              placeholder_text_color = 'light grey',
                                              font = ('Arial', 12),
                                              width = 90)
        self.investment_period_years.grid(row = 6, column = 0, padx = 10, pady = 5, sticky = 'w')

        # Set up months
        self.investment_months = ctk.CTkLabel(self.main_contribution, text = 'Months:', 
                                              font = ('Arial', 12))
        self.investment_months.grid(row = 5, column = 0, padx = (120,0), pady = 5, sticky = 'w')

        self.string_var = StringVar(self.main_contribution, value = '0')
        self.investment_period_months = ctk.CTkEntry(self.main_contribution,
                                              placeholder_text_color = 'light grey',
                                              font = ('Arial', 12), textvariable = self.string_var,
                                              width = 90)
        
        self.investment_period_months.grid(row = 6, column = 0, padx = (120,0), pady = 5, sticky = 'w')

        """
        Set up additional investment contribution frame
        """

        self.additional_contribution = ctk.CTkFrame(self.tab_1, corner_radius=10,
                                                    width= 400, fg_color = 'black',
                                                    height = 170)
        self.additional_contribution.grid(row = 1, column = 0, padx = 10, pady = 10, sticky = 'nw')
        
        # Set up label and entry box for monthly deposit 
        self.monthly_deposit_header = ctk.CTkLabel(self.additional_contribution, 
                                                   text = 'Monthly Deposit: ',
                                                   font = ('Arial', 12))
        self.monthly_deposit_header.grid(row = 2, column = 0, padx = 10, pady = (10,0), sticky = 'w')

        self.monthly_deposit = ctk.CTkEntry(self.additional_contribution, placeholder_text= 'Enter the monthly deposit amount: ',
                                              placeholder_text_color= 'light grey',
                                              font = ('Arial', 12), width = 220)
        self.monthly_deposit.grid(row = 3, column = 0, padx = 10, pady = (10,0), sticky = 'ew') 

        # Set up future value of investment calculation
        def future_value():
            try:
                # get initial investment amount
                self.ii = float(self.initial_investment.get())

                # Convert interest rate from percentage into decimal
                self.ir = float(self.interest_rate.get())/100

                # Set up different interest rate cases
                if self.interest_rate_combobox.get() == 'daily':
                    self.ir = self.ir*30
                elif self.interest_rate_combobox.get() == 'yearly':
                    self.ir = self.ir/12
                elif self.interest_rate_combobox.get() == 'quarterly':
                    self.ir = self.ir/3
                elif self.interest_rate_combobox.get() == 'monthly':
                    self.ir = self.ir

                # Add the years and months to the investment period
                self.y = float(self.investment_period_years.get()) + float(self.investment_period_months.get())/12
                self.y = round(self.y,2)

                # Add monthly deposit
                self.md = float(self.monthly_deposit.get())

                # Calculate the yield
                self.future_value = round((self.ii)*(1+((self.ir)/12))**(12*(self.y)) +
                            ((self.md)*((1+(self.ir)/12)**(12*(self.y))-1))/((self.ir)/12), 2)
                
                if isinstance(self.future_value, float):
                    messagebox.showinfo(title = 'Future Yield', 
                                message = (f'The investment yield is ${self.future_value} after {(self.y)} years.'))
                else:
                    messagebox.showinfo(title = 'Error', 
                                message = ('Please re-enter values'))
                    print(self.future_value)
    
                self.x_years_compound = [0]
                self.compounding_future_yield = [0]

                # Set up axes for graph
                if self.investment_period_months.get() == '0' and int(self.investment_period_years.get()) > 20:
                    for year in range(0, int(self.investment_period_years.get()), 10):
                        self.x_years_compound.append(year+10)
                        self.compounding_future_yield.append(round((self.ii)*(1+((self.ir)/12))**(12*(year+10)) +
                                ((self.md)*((1+(self.ir)/12)**(12*(year+10))-1))/((self.ir)/12), 2))
                elif self.investment_period_months.get() == '0' and int(self.investment_period_years.get()) <= 20:
                    for year in range(0, int(self.investment_period_years.get())):
                        self.x_years_compound.append(year)
                        self.compounding_future_yield.append(round((self.ii)*(1+((self.ir)/12))**(12*(year)) +
                                ((self.md)*((1+(self.ir)/12)**(12*(year))-1))/((self.ir)/12), 2))
                """
                Set up compound interest graph 
                """
                try:
                    #reset window to show plot
                    self.my_tab.configure(width = '900')
                    self.geometry('900x520')
                    # set up frame
                    self.compound_graph_frame = ctk.CTkFrame(self.tab_1, height = 400, width = 300)
                    self.compound_graph_frame.grid(row = 0, column = 1, rowspan = 3, padx = 10, pady = 10, sticky = 'ne')

                    # Set up special canvas to imbed matplotlib graph
                    self.fig = Figure(figsize = (7,5), dpi = 70)
                    self.ax = self.fig.add_subplot(111)
                    self.ax.set_title("Compound Interest")
                    self.ax.set_xlabel("Years")
                    self.ax.set_ylabel("Interest Yield (USD)")
                    self.ax.grid(color = 'black')
                    self.ax.plot(self.x_years_compound, self.compounding_future_yield, 
                                 color = 'green', marker = 'o')
                    self.compound_canvas = FigureCanvasTkAgg(self.fig, master = self.compound_graph_frame)
                    self.compound_canvas.draw()
                    self.compound_canvas.get_tk_widget().grid(row = 0, column = 1, rowspan = 3, padx = 10, pady = 10, sticky = 'ne') 
                except Exception as e:
                    print(e)      
            except Exception as e:
                print(e)
                messagebox.showinfo(title = 'Input Error', 
                                message = ('Please enter the correct information within the fields.'))
        
        def clear():
            self.entries = {self.initial_investment, self.interest_rate, 
                            self.investment_period_months, self.investment_period_years,
                              self.monthly_deposit}
            for self.entry in self.entries:
                self.entry.delete(0, END)
            self.my_tab.configure(width = '400')
            self.geometry('400x520')
            self.compound_canvas.get_tk_widget().destroy()
            self.compound_graph_frame.destroy()
            self.investment_period_months.insert(0, '0')
            
        # Set up a button that determines the future value of the investment
        self.find_yield_button = ctk.CTkButton(self.additional_contribution, 
                                               text = 'Get Result', corner_radius = 50, width = 320, 
                                               fg_color = 'forest green', command = future_value)
        self.find_yield_button.grid(row = 4, column = 0, padx = 10, pady =(10,0), sticky = 'sew', columnspan = 3)

        # Set up a button that clears values
        self.clear_button = ctk.CTkButton(self.additional_contribution, 
                                          text = 'Reset Values',
                                          corner_radius=50, width = 320,
                                           fg_color= 'dark red', command = clear)
        self.clear_button.grid(row = 5, column = 0, padx = 10, pady = (10,0), sticky = 'sew', columnspan = 3)
         
            
        """
        Set up simple interest tab
        """
        # set up frame to hold starting balance and interest rate
        self.balance_frame = ctk.CTkFrame(self.tab_2, corner_radius=30,
                                     width = 220, height  = 300, fg_color= 'black')
        self.balance_frame.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = 'nw')
        
        # set up starting balance
        self.starting_balance_header = ctk.CTkLabel(self.balance_frame, text = 'Starting Balance')
        self.starting_balance_header.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = 'w')

        self.starting_balance_entry = ctk.CTkEntry(self.balance_frame, 
                                                   placeholder_text='Enter the balance amount:',
                                                   placeholder_text_color= 'light grey',
                                                   font = ('Arial', 12), width = 220)
        self.starting_balance_entry.grid(row = 1, column = 0, padx = 10, pady = (10,0), sticky = 'w')

        # set up interest rate
        self.initial_rate_header2 = ctk.CTkLabel(self.balance_frame, 
                                                text = 'Interest Rate: ',
                                                font = ('Arial', 12))
        self.initial_rate_header2.grid(row = 2, column = 0, padx = 10, pady = (10,0), sticky = 'w')

        self.interest_rate2 = ctk.CTkEntry(self.balance_frame, placeholder_text = 'Enter the interest rate percentage: ',
                                        placeholder_text_color= 'light grey',
                                        font = ('Arial', 12),
                                        width = 220)
        self.interest_rate2.grid(row = 3, column = 0, padx = 10, pady = (10,0), sticky = 'ew')

        """
        Set up simple interest frame for time period and final result button, clear fields button
        """
        # set up other frame
        self.secondary_balance_frame = ctk.CTkFrame(self.tab_2, corner_radius=10,
                                                    fg_color = 'black',
                                                    height = 300, width = 400)
        self.secondary_balance_frame.grid(row = 1, column = 0, padx = 10, pady = (10,0), sticky = 'nw')
        
        # set up investment period
        self.investment_period_header2 = ctk.CTkLabel(self.secondary_balance_frame, 
                                                     text = 'Investment Length: ',
                                                     font = ('Arial', 12))
        self.investment_period_header2.grid(row = 0, column = 0, padx = 10, pady = (10,0), sticky = 'w')

        self.investment_years2 = ctk.CTkLabel(self.secondary_balance_frame, text = 'Years:', 
                                              font = ('Arial', 12))
        self.investment_years2.grid(row = 1, column = 0, padx = 10, pady = 5, sticky = 'w')

        self.investment_period_years2 = ctk.CTkEntry(self.secondary_balance_frame,
                                              placeholder_text_color = 'light grey',
                                              font = ('Arial', 12),
                                              width = 90)
        self.investment_period_years2.grid(row = 2, column = 0, padx = 10, pady = 5, sticky = 'w')

         # Set up future value of investment calculation
        def future_value_simple():
            try:
                # get value of starting balance as a float
                self.ii = float(self.starting_balance_entry.get())

                # Convert interest rate from percentage into decimal
                self.ir = float(self.interest_rate2.get())/100 

                # Add the years to the investment period
                self.y = float(self.investment_period_years2.get())

                # Calculate the yield
                self.future_value_simple = round((self.ii)*(1+((self.ir)*self.y)), 2)
                
                if isinstance(self.future_value_simple, float):
                    messagebox.showinfo(title = 'Future Yield', 
                                message = (f'The investment yield is ${self.future_value} after {(self.y)} years.'))
                else:
                    messagebox.showinfo(title = 'Error', 
                                message = ('Please re-enter values'))
                    print(self.future_value)
                
                self.x_years_simple = [0]
                self.simple_future_yield = [0]

            # Set up axes for graph
                if int(self.investment_period_years2.get()) > 20:
                    for year in range(0, int(self.investment_period_years2.get()), 10):
                        self.x_years_simple.append(year+10)
                        self.simple_future_yield.append(round((self.ii)*(1+((self.ir)*self.y)), 2))
                elif int(self.investment_period_years2.get()) <= 20:
                    for year in range(0, int(self.investment_period_years2.get())):
                        self.x_years_simple.append(year)
                        self.simple_future_yield.append(round((self.ii)*(1+((self.ir)*self.y)), 2))
                
                """
                Set up simple interest graph 
                """
                try:
                    #reset window to show plot
                    self.my_tab.configure(width = '900')
                    self.geometry('900x520')
                    # set up frame
                    self.simple_graph_frame = ctk.CTkFrame(self.tab_2, height = 400, width = 300)
                    self.simple_graph_frame.grid(row = 0, column = 1, rowspan = 3, padx = 10, pady = 10, sticky = 'ne')

                    # Set up special canvas to imbed matplotlib graph
                    self.fig = Figure(figsize = (7,5), dpi = 70)
                    self.ax = self.fig.add_subplot(111)
                    self.ax.set_title("Simple Interest")
                    self.ax.set_xlabel("Years")
                    self.ax.set_ylabel("Interest Yield (USD)")
                    self.ax.grid(color = 'black')
                    self.ax.plot(self.x_years_simple, self.simple_future_yield, 
                                 color = 'green', marker = 'o')
                    self.simple_canvas = FigureCanvasTkAgg(self.fig, master = self.simple_graph_frame)
                    self.simple_canvas.draw()
                    self.simple_canvas.get_tk_widget().grid(row = 0, column = 1, rowspan = 3, padx = 10, pady = 10, sticky = 'ne') 
                except Exception as e:
                    print(e)
            except Exception as e:
                print(e)
                messagebox.showinfo(title = 'Input Error', 
                                message = ('Please enter the correct information within the fields.'))

        
        def clear_simple():
            self.entries = {self.starting_balance_entry, self.interest_rate2, 
                            self.investment_period_years2}
            for self.entry in self.entries:
                self.entry.delete(0, END)
            self.my_tab.configure(width = '400')
            self.geometry('400x520')
            self.simple_canvas.get_tk_widget().destroy()
            self.simple_graph_frame.destroy()
            
         # Set up a button that determines the future value of the investment
        self.find_yield_button = ctk.CTkButton(self.secondary_balance_frame, 
                                               text = 'Get Result', corner_radius = 50, width = 320, 
                                               fg_color = 'forest green', command = future_value_simple)
        self.find_yield_button.grid(row = 5, column = 0, padx = 10, pady =(10,0), sticky = 'sew', columnspan = 3)

        # Set up a button that clears values
        self.clear_button = ctk.CTkButton(self.secondary_balance_frame, 
                                          text = 'Reset Values',
                                          corner_radius=50, width = 320,
                                           fg_color= 'dark red', command = clear_simple)
        self.clear_button.grid(row = 6, column = 0, padx = 10, pady = (10,0), sticky = 'sew', columnspan = 3)

app = Compound_Interest_GUI()
app.mainloop()  
