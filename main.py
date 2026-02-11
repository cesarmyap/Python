import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import sys
import os

# Add modules directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

# Import modules
try:
    from modules.clients import ClientsModule
    from modules.suppliers import SuppliersModule
    from modules.inventory import InventoryModule
    from modules.sales import SalesModule
    from modules.purchasing import PurchasingModule
    from modules.accounting import AccountingModule
    from database import create_database
    from styles import apply_style
except ImportError as e:
    print(f"Import error: {e}")


    # Create dummy classes for testing
    class ClientsModule:
        def __init__(self, parent): pass


    class SuppliersModule:
        def __init__(self, parent): pass


    class InventoryModule:
        def __init__(self, parent): pass


    class SalesModule:
        def __init__(self, parent): pass


    class PurchasingModule:
        def __init__(self, parent): pass


    class AccountingModule:
        def __init__(self, parent): pass


class ERPSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("ERP System - Complete Business Management")
        self.root.geometry("1200x700")

        # Create database
        create_database()

        # Apply styling
        apply_style()

        # Setup main window
        self.setup_menu()
        self.setup_main_frame()
        self.setup_status_bar()

        # Initialize modules
        self.current_module = None

        # Show dashboard initially
        self.show_dashboard()

    def setup_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Dashboard", command=self.show_dashboard)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Modules Menu
        modules_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Modules", menu=modules_menu)
        modules_menu.add_command(label="Clients Management", command=self.show_clients)
        modules_menu.add_command(label="Suppliers Management", command=self.show_suppliers)
        modules_menu.add_command(label="Inventory", command=self.show_inventory)
        modules_menu.add_command(label="Sales & Quotations", command=self.show_sales)
        modules_menu.add_command(label="Purchasing", command=self.show_purchasing)
        modules_menu.add_command(label="Accounting", command=self.show_accounting)

        # Reports Menu
        reports_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Reports", menu=reports_menu)
        reports_menu.add_command(label="Sales Statistics", command=self.show_sales_stats)
        reports_menu.add_command(label="Inventory Report", command=self.show_inventory_report)
        reports_menu.add_command(label="Financial Reports", command=self.show_financial_reports)

        # Help Menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="User Guide", command=self.show_user_guide)

    def setup_main_frame(self):
        # Main container
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Header
        header_frame = ttk.Frame(self.main_container)
        header_frame.pack(fill=tk.X, padx=5, pady=(5, 10))

        ttk.Label(header_frame, text="ERP SYSTEM",
                  font=("Arial", 20, "bold")).pack(side=tk.LEFT)

        # Quick access buttons
        quick_frame = ttk.Frame(header_frame)
        quick_frame.pack(side=tk.RIGHT)

        buttons = [
            ("📊 Dashboard", self.show_dashboard),
            ("👥 Clients", self.show_clients),
            ("📦 Inventory", self.show_inventory),
            ("💰 Sales", self.show_sales),
            ("📋 Orders", self.show_purchasing)
        ]

        for text, command in buttons:
            ttk.Button(quick_frame, text=text, command=command,
                       width=12).pack(side=tk.LEFT, padx=2)

    def setup_status_bar(self):
        self.status_bar = ttk.Frame(self.root, relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.status_label = ttk.Label(self.status_bar, text="Ready")
        self.status_label.pack(side=tk.LEFT, padx=5)

        ttk.Label(self.status_bar, text=f"Date: {datetime.now().strftime('%Y-%m-%d')}").pack(side=tk.RIGHT, padx=5)

    def clear_main_area(self):
        for widget in self.main_container.winfo_children():
            if widget not in [self.main_container.winfo_children()[0], self.main_container.winfo_children()[-1]]:
                widget.destroy()

    def show_dashboard(self):
        self.clear_main_area()

        dashboard_frame = ttk.Frame(self.main_container)
        dashboard_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Dashboard Title
        ttk.Label(dashboard_frame, text="Dashboard Overview",
                  font=("Arial", 16, "bold")).pack(pady=(0, 20))

        # Stats Frame
        stats_frame = ttk.Frame(dashboard_frame)
        stats_frame.pack(fill=tk.X, pady=(0, 20))

        # Statistics cards
        stats = [
            ("Total Clients", "150", "👥"),
            ("Active Suppliers", "45", "🏭"),
            ("Inventory Items", "320", "📦"),
            ("Pending Orders", "12", "📋"),
            ("Today's Sales", "$8,450", "💰"),
            ("Monthly Revenue", "$125,000", "📈")
        ]

        for i, (title, value, icon) in enumerate(stats):
            card = ttk.Frame(stats_frame, relief=tk.RAISED, borderwidth=2)
            card.grid(row=i // 3, column=i % 3, padx=10, pady=10, sticky="nsew")

            ttk.Label(card, text=icon, font=("Arial", 24)).pack(pady=(10, 5))
            ttk.Label(card, text=value, font=("Arial", 18, "bold")).pack()
            ttk.Label(card, text=title, font=("Arial", 10)).pack(pady=(0, 10))

        # Recent Activities
        activities_frame = ttk.LabelFrame(dashboard_frame, text="Recent Activities")
        activities_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        columns = ("Time", "Activity", "User", "Status")
        tree = ttk.Treeview(activities_frame, columns=columns, show="headings", height=8)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        # Sample data
        activities = [
            ("10:30 AM", "New Quotation Created #QT-00123", "John Doe", "Pending"),
            ("09:45 AM", "Purchase Order Confirmed #PO-00456", "Jane Smith", "Confirmed"),
            ("09:15 AM", "Inventory Updated - Product XYZ", "Admin", "Completed"),
            ("Yesterday", "Delivery Note #DN-00789", "Mike Brown", "Delivered"),
            ("Yesterday", "Invoice Generated #INV-00321", "Sarah Lee", "Paid")
        ]

        for activity in activities:
            tree.insert("", tk.END, values=activity)

        scrollbar = ttk.Scrollbar(activities_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.status_label.config(text="Dashboard loaded")

    def show_clients(self):
        self.clear_main_area()
        self.current_module = ClientsModule(self.main_container)
        self.status_label.config(text="Clients Management Module")

    def show_suppliers(self):
        self.clear_main_area()
        self.current_module = SuppliersModule(self.main_container)
        self.status_label.config(text="Suppliers Management Module")

    def show_inventory(self):
        self.clear_main_area()
        self.current_module = InventoryModule(self.main_container)
        self.status_label.config(text="Inventory Management Module")

    def show_sales(self):
        self.clear_main_area()
        self.current_module = SalesModule(self.main_container)
        self.status_label.config(text="Sales & Quotations Module")

    def show_purchasing(self):
        self.clear_main_area()
        self.current_module = PurchasingModule(self.main_container)
        self.status_label.config(text="Purchasing Module")

    def show_accounting(self):
        self.clear_main_area()
        self.current_module = AccountingModule(self.main_container)
        self.status_label.config(text="Accounting Module")

    def show_sales_stats(self):
        messagebox.showinfo("Sales Statistics", "Sales statistics report will be displayed here.")

    def show_inventory_report(self):
        messagebox.showinfo("Inventory Report", "Inventory report will be displayed here.")

    def show_financial_reports(self):
        messagebox.showinfo("Financial Reports", "Financial reports will be displayed here.")

    def show_about(self):
        about_text = """ERP System v1.0

Complete Business Management Solution
Developed in Python with Tkinter

Features:
• Clients Management
• Suppliers Management
• Inventory Control
• Sales & Quotations
• Purchasing
• Accounting

© 2024 All Rights Reserved"""
        messagebox.showinfo("About ERP System", about_text)

    def show_user_guide(self):
        messagebox.showinfo("User Guide", "User guide documentation will be available here.")


def main():
    root = tk.Tk()
    app = ERPSystem(root)
    root.mainloop()


if __name__ == "__main__":
    main()
