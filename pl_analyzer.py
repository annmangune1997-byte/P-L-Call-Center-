import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import pandas as pd
import os
from datetime import datetime

# --- FILE NAMES FOR DATA STORAGE ---
# These files will be created automatically in the same folder as the script.
ORDERS_FILE = 'orders_data.csv'
EXPENSES_FILE = 'expenses_data.csv'

# --- DATA INITIALIZATION ---
# Create CSV files with headers if they don't exist, ensuring the system can run on the first try.
def initialize_data_files():
    """Creates the necessary CSV files if they don't already exist."""
    if not os.path.exists(ORDERS_FILE):
        pd.DataFrame(columns=[
            'date', 'product_sales', 'delivery_fee', 'other_fees', 
            'discounts', 'cogs', 'packaging_cost'
        ]).to_csv(ORDERS_FILE, index=False)

    if not os.path.exists(EXPENSES_FILE):
        pd.DataFrame(columns=[
            'date_saved', 'people_costs', 'delivery_vehicle_costs', 
            'technology_costs', 'marketing_costs', 'rent_utilities', 'other_overhead'
        ]).to_csv(EXPENSES_FILE, index=False)

# --- MAIN APPLICATION CLASS ---
class PLAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("P&L Analyzer for Home Delivery")
        self.root.geometry("850x650")

        initialize_data_files()

        # Create a notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Create tabs
        self.tab_orders = ttk.Frame(self.notebook)
        self.tab_expenses = ttk.Frame(self.notebook)
        self.tab_report = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_orders, text="1. Enter Order Data")
        self.notebook.add(self.tab_expenses, text="2. Enter Monthly Expenses")
        self.notebook.add(self.tab_report, text="3. Analysis & Report")

        self.create_orders_tab()
        self.create_expenses_tab()
        self.create_report_tab()

        # Status bar at the bottom
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.update_status("Ready. Enter data and click 'Generate P&L Report'.")

    def update_status(self, message):
        """Updates the status bar message."""
        self.status_var.set(message)
        self.root.update_idletasks()

    def create_orders_tab(self):
        """Creates the UI for entering individual order data."""
        frame = ttk.LabelFrame(self.tab_orders, text="New Order Details", padding=10)
        frame.pack(fill='x', padx=20, pady=20)

        # --- Revenue Fields ---
        ttk.Label(frame, text="--- Revenue ---", font=('Helvetica', 10, 'bold')).grid(row=0, column=0, columnspan=2, sticky='w', pady=(0,10))
        ttk.Label(frame, text="Product Sales ($):").grid(row=1, column=0, sticky='w', padx=5)
        self.product_sales_entry = ttk.Entry(frame, width=20)
        self.product_sales_entry.grid(row=1, column=1, padx=5, pady=2)
        self.product_sales_entry.insert(0, "0.00")

        ttk.Label(frame, text="Delivery Fee ($):").grid(row=2, column=0, sticky='w', padx=5)
        self.delivery_fee_entry = ttk.Entry(frame, width=20)
        self.delivery_fee_entry.grid(row=2, column=1, padx=5, pady=2)
        self.delivery_fee_entry.insert(0, "0.00")

        ttk.Label(frame, text="Other Fees ($):").grid(row=3, column=0, sticky='w', padx=5)
        self.other_fees_entry = ttk.Entry(frame, width=20)
        self.other_fees_entry.grid(row=3, column=1, padx=5, pady=2)
        self.other_fees_entry.insert(0, "0.00")

        ttk.Label(frame, text="Discounts ($):").grid(row=4, column=0, sticky='w', padx=5)
        self.discounts_entry = ttk.Entry(frame, width=20)
        self.discounts_entry.grid(row=4, column=1, padx=5, pady=2)
        self.discounts_entry.insert(0, "0.00")

        # --- COGS Fields ---
        ttk.Label(frame, text="--- Cost of Goods Sold (COGS) ---", font=('Helvetica', 10, 'bold')).grid(row=5, column=0, columnspan=2, sticky='w', pady=(15,10))
        ttk.Label(frame, text="Product Cost ($):").grid(row=6, column=0, sticky='w', padx=5)
        self.cogs_entry = ttk.Entry(frame, width=20)
        self.cogs_entry.grid(row=6, column=1, padx=5, pady=2)
        self.cogs_entry.insert(0, "0.00")

        ttk.Label(frame, text="Packaging Cost ($):").grid(row=7, column=0, sticky='w', padx=5)
        self.packaging_cost_entry = ttk.Entry(frame, width=20)
        self.packaging_cost_entry.grid(row=7, column=1, padx=5, pady=2)
        self.packaging_cost_entry.insert(0, "0.00")

        # --- Buttons ---
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=8, column=0, columnspan=2, pady=20)
        add_button = ttk.Button(button_frame, text="Add Order", command=self.add_order)
        add_button.pack(side=tk.LEFT, padx=5)
        clear_button = ttk.Button(button_frame, text="Clear Form", command=self.clear_order_form)
        clear_button.pack(side=tk.LEFT, padx=5)

    def create_expenses_tab(self):
        """Creates the UI for entering monthly operating expenses."""
        frame = ttk.LabelFrame(self.tab_expenses, text="Monthly Operating Expenses", padding=10)
        frame.pack(fill='x', padx=20, pady=20)
        
        self.expense_last_saved_label = ttk.Label(frame, text="No data saved yet.", font=('Helvetica', 9, 'italic'))
        self.expense_last_saved_label.grid(row=0, column=0, columnspan=2, pady=(0,10))
        self.update_expense_saved_date()

        self.expense_entries = {}
        expense_labels = {
            'people_costs': 'People Costs (Salaries, Wages, Benefits):',
            'delivery_vehicle_costs': 'Delivery & Vehicle Costs (Fuel, Insurance, Maintenance):',
            'technology_costs': 'Technology Costs (Software, Phone, Internet):',
            'marketing_costs': 'Marketing Costs (Ads, Promotions, Discounts):',
            'rent_utilities': 'Rent & Utilities:',
            'other_overhead': 'Other Overhead (Supplies, Fees, Insurance):'
        }

        for i, (key, label) in enumerate(expense_labels.items()):
            ttk.Label(frame, text=label).grid(row=i+1, column=0, sticky='w', padx=5, pady=5)
            entry = ttk.Entry(frame, width=30)
            entry.grid(row=i+1, column=1, padx=5, pady=5)
            entry.insert(0, "0.00")
            self.expense_entries[key] = entry

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=len(expense_labels)+1, column=0, columnspan=2, pady=20)
        save_button = ttk.Button(button_frame, text="Save Monthly Expenses", command=self.save_expenses)
        save_button.pack(side=tk.LEFT, padx=5)
        clear_expenses_button = ttk.Button(button_frame, text="Clear Form", command=self.clear_expense_form)
        clear_expenses_button.pack(side=tk.LEFT, padx=5)

    def create_report_tab(self):
        """Creates the UI for displaying the analysis report."""
        frame = ttk.Frame(self.tab_report)
        frame.pack(fill='both', expand=True, padx=20, pady=20)

        generate_button = ttk.Button(frame, text="Generate P&L Report", command=self.generate_report)
        generate_button.pack(pady=10)

        self.report_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=90, height=30, font=('Courier', 10))
        self.report_text.pack(fill='both', expand=True)

    def clear_order_form(self):
        """Resets all entry fields in the order form to 0.00."""
        for entry in [self.product_sales_entry, self.delivery_fee_entry, self.other_fees_entry, self.discounts_entry, self.cogs_entry, self.packaging_cost_entry]:
            entry.delete(0, tk.END)
            entry.insert(0, "0.00")
        self.update_status("Order form cleared.")

    def clear_expense_form(self):
        """Resets all entry fields in the expense form to 0.00."""
        for entry in self.expense_entries.values():
            entry.delete(0, tk.END)
            entry.insert(0, "0.00")
        self.update_status("Expense form cleared.")

    def add_order(self):
        """Adds a single order's data to the CSV file."""
        try:
            new_order = {
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'product_sales': float(self.product_sales_entry.get()),
                'delivery_fee': float(self.delivery_fee_entry.get()),
                'other_fees': float(self.other_fees_entry.get()),
                'discounts': float(self.discounts_entry.get()),
                'cogs': float(self.cogs_entry.get()),
                'packaging_cost': float(self.packaging_cost_entry.get())
            }
            df = pd.read_csv(ORDERS_FILE)
            df = pd.concat([df, pd.DataFrame([new_order])], ignore_index=True)
            df.to_csv(ORDERS_FILE, index=False)
            
            self.clear_order_form()
            self.update_status(f"Order added successfully. Total orders: {len(df)}")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers in all fields.")

    def save_expenses(self):
        """Saves the monthly operating expenses to the CSV file."""
        try:
            expenses_data = {key: float(entry.get()) for key, entry in self.expense_entries.items()}
            expenses_data['date_saved'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            df = pd.DataFrame([expenses_data])
            df.to_csv(EXPENSES_FILE, index=False)
            self.update_expense_saved_date()
            self.update_status("Monthly expenses saved successfully.")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers in all expense fields.")

    def update_expense_saved_date(self):
        """Updates the label showing when expenses were last saved."""
        try:
            df = pd.read_csv(EXPENSES_FILE)
            if not df.empty:
                last_saved_date = df['date_saved'].iloc[0]
                self.expense_last_saved_label.config(text=f"Last saved on: {last_saved_date}")
        except (FileNotFoundError, pd.errors.EmptyDataError, KeyError):
            self.expense_last_saved_label.config(text="No data saved yet.")


    def generate_report(self):
        """Reads data, performs analysis, and displays the report."""
        self.update_status("Generating report... please wait.")
        self.report_text.delete('1.0', tk.END)
        
        # --- Load Data ---
        try:
            orders_df = pd.read_csv(ORDERS_FILE)
            expenses_df = pd.read_csv(EXPENSES_FILE)
        except FileNotFoundError:
            self.report_text.insert(tk.END, "Error: Data files not found. Please enter some data first.")
            self.update_status("Error: Data files not found.")
            return

        if orders_df.empty:
            self.report_text.insert(tk.END, "No order data available to analyze. Please enter some orders first.")
            self.update_status("No order data to analyze.")
            return
        if expenses_df.empty:
            self.report_text.insert(tk.END, "No expense data available. Please enter monthly expenses first.")
            self.update_status("No expense data to analyze.")
            return

        # --- P&L Calculations ---
        # Revenue
        total_revenue = (orders_df['product_sales'] + orders_df['delivery_fee'] + orders_df['other_fees'] - orders_df['discounts']).sum()
        
        # COGS
        total_cogs = (orders_df['cogs'] + orders_df['packaging_cost']).sum()
        
        # Gross Profit
        gross_profit = total_revenue - total_cogs
        gross_profit_margin = (gross_profit / total_revenue * 100) if total_revenue > 0 else 0
        
        # Operating Expenses
        total_expenses = expenses_df.iloc[0, 1:].sum() # Sum all columns except the date
        
        # Net Profit / Loss
        net_profit = gross_profit - total_expenses

        # --- Key Metrics ---
        num_orders = len(orders_df)
        avg_order_value = total_revenue / num_orders if num_orders > 0 else 0
        total_delivery_fees_collected = orders_df['delivery_fee'].sum()
        total_delivery_costs = expenses_df['delivery_vehicle_costs'].sum()
        cost_per_delivery = total_delivery_costs / num_orders if num_orders > 0 else 0
        avg_delivery_fee_collected = total_delivery_fees_collected / num_orders if num_orders > 0 else 0
        people_costs = expenses_df['people_costs'].sum()
        labor_cost_percent = (people_costs / total_revenue * 100) if total_revenue > 0 else 0

        # --- Generate Report Text ---
        report = f"""
{'='*90}
{'PROFIT & LOSS (P&L) REPORT':^90}
{'='*90}

--- FINANCIAL SUMMARY ---
{'Total Revenue:':<35} ${total_revenue:>50,.2f}
  {'- Product Sales:':<35} ${orders_df['product_sales'].sum():>50,.2f}
  {'- Delivery Fees:':<35} ${total_delivery_fees_collected:>50,.2f}
  {'- Other Fees:':<35} ${orders_df['other_fees'].sum():>50,.2f}
  {'- Discounts:':<35} (${-orders_df['discounts'].sum():>49,.2f})
{'':<35}{'-'*50}
{'Cost of Goods Sold (COGS):':<35} (${-total_cogs:>49,.2f})
{'':<35}{'='*50}
{'Gross Profit:':<35} ${gross_profit:>50,.2f}
{'Gross Profit Margin:':<35} {gross_profit_margin:>48.2f}%
{'':<35}
{'Operating Expenses:':<35} (${-total_expenses:>49,.2f})
  {'- People Costs:':<35} (${-people_costs:>49,.2f})
  {'- Delivery & Vehicle Costs:':<35} (${-total_delivery_costs:>49,.2f})
  {'- Technology Costs:':<35} (${-expenses_df['technology_costs'].sum():>49,.2f})
  {'- Marketing Costs:':<35} (${-expenses_df['marketing_costs'].sum():>49,.2f})
  {'- Rent & Utilities:':<35} (${-expenses_df['rent_utilities'].sum():>49,.2f})
  {'- Other Overhead:':<35} (${-expenses_df['other_overhead'].sum():>49,.2f})
{'':<35}{'-'*50}
{'NET PROFIT / (LOSS):':<35} ${net_profit:>50,.2f}

{'='*90}
{'KEY PERFORMANCE METRICS':^90}
{'='*90}
{'Total Number of Orders:':<35} {num_orders:>50}
{'Average Order Value (AOV):':<35} ${avg_order_value:>50,.2f}
{'Average Delivery Fee Collected:':<35} ${avg_delivery_fee_collected:>50,.2f}
{'Calculated Cost Per Delivery:':<35} ${cost_per_delivery:>50,.2f}
{'Labor Cost as % of Revenue:':<35} {labor_cost_percent:>48.2f}%

{'='*90}
{'SYSTEM ANALYSIS & SUGGESTIONS':^90}
{'='*90}
"""
        self.report_text.insert(tk.END, report)

        # --- Generate Suggestions ---
        suggestions = ""
        if net_profit >= 0:
            suggestions = "\n>>> CONGRATULATIONS! You are profitable. <<<\n\n"
            suggestions += "To improve further:\n"
            if gross_profit_margin < 50:
                suggestions += "- Consider increasing prices or finding cheaper suppliers to boost your Gross Profit Margin.\n"
            if labor_cost_percent > 30:
                suggestions += "- Your labor costs are a bit high. Look into optimizing staff schedules.\n"
        else: # Net Loss
            suggestions = "\n>>> ACTION REQUIRED: You are currently operating at a loss. <<<\n\n"
            suggestions += "Here are the most likely problem areas and what to change:\n\n"
            
            # Check Gross Profit
            if gross_profit_margin < 40:
                suggestions += f"[PROBLEM] Low Gross Profit Margin ({gross_profit_margin:.2f}%). Your core service is not profitable.\n"
                suggestions += "  [SUGGESTION] RAISE PRICES: Increase product prices or delivery fees.\n"
                suggestions += "  [SUGGESTION] CUT COGS: Negotiate with suppliers for better prices or reduce waste.\n\n"
            
            # Check Delivery Costs
            if cost_per_delivery > avg_delivery_fee_collected:
                suggestions += "[PROBLEM] Delivery costs are higher than the fees you collect.\n"
                suggestions += "  [SUGGESTION] INCREASE FEES: Raise your delivery fee or set a minimum order value for delivery.\n"
                suggestions += "  [SUGGESTION] OPTIMIZE ROUTES: Use routing software to save fuel and time.\n\n"

            # Check Labor Costs
            if labor_cost_percent > 35:
                suggestions += f"[PROBLEM] High labor costs ({labor_cost_percent:.2f}% of revenue).\n"
                suggestions += "  [SUGGESTION] OPTIMIZE SCHEDULING: Schedule more staff during peak hours and fewer during slow times.\n"
                suggestions += "  [SUGGESTION] IMPROVE EFFICIENCY: Train staff to handle calls and deliveries faster.\n\n"

            # Check Marketing
            marketing_cost = expenses_df['marketing_costs'].sum()
            if marketing_cost > 0 and total_revenue > 0:
                if (marketing_cost / total_revenue) > 0.10: # If marketing is >10% of revenue
                    suggestions += "[PROBLEM] High marketing spend relative to revenue.\n"
                    suggestions += "  [SUGGESTION] FOCUS ON ROI: Stop ads that aren't bringing in customers. Track your marketing results.\n\n"

        if not suggestions:
            suggestions = "No specific suggestions at this time. Continue monitoring your metrics."

        self.report_text.insert(tk.END, suggestions)
        self.update_status("P&L Report generated. Review the analysis.")

# --- RUN THE APPLICATION ---
if __name__ == "__main__":
    root = tk.Tk()
    app = PLAnalyzerApp(root)
    root.mainloop()
