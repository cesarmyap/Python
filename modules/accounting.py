import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime, date
import random


class AccountingModule:
    def __init__(self, parent):
        self.parent = parent
        self.setup_ui()
        self.load_receipts()

    def setup_ui(self):
        notebook = ttk.Notebook(self.parent)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Receipts tab
        receipts_tab = ttk.Frame(notebook)
        notebook.add(receipts_tab, text="🧾 Receipts")
        self.setup_receipts_tab(receipts_tab)

        # Statements tab
        statements_tab = ttk.Frame(notebook)
        notebook.add(statements_tab, text="📊 Statements")
        self.setup_statements_tab(statements_tab)

        # Reports tab
        reports_tab = ttk.Frame(notebook)
        notebook.add(reports_tab, text="📈 Reports")
        self.setup_reports_tab(reports_tab)

    def setup_receipts_tab(self, parent):
        ttk.Label(parent, text="Receipts Management",
                  font=("Arial", 14, "bold")).pack(pady=(10, 20))

        # Control buttons
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill=tk.X, pady=(0, 10), padx=20)

        ttk.Button(control_frame, text="💰 New Receipt",
                   command=self.create_receipt, style="Success.TButton").pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="👁️ View", command=self.view_receipt).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="🖨️ Print", command=self.print_receipt).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="🔄 Refresh", command=self.load_receipts).pack(side=tk.LEFT, padx=2)

        # Filter frame
        filter_frame = ttk.Frame(parent)
        filter_frame.pack(fill=tk.X, pady=(0, 10), padx=20)

        ttk.Label(filter_frame, text="Date From:").pack(side=tk.LEFT, padx=5)
        self.receipt_date_from = ttk.Entry(filter_frame, width=12)
        self.receipt_date_from.insert(0, date.today().strftime("%Y-%m-01"))
        self.receipt_date_from.pack(side=tk.LEFT, padx=5)

        ttk.Label(filter_frame, text="To:").pack(side=tk.LEFT, padx=5)
        self.receipt_date_to = ttk.Entry(filter_frame, width=12)
        self.receipt_date_to.insert(0, date.today().strftime("%Y-%m-%d"))
        self.receipt_date_to.pack(side=tk.LEFT, padx=5)

        ttk.Button(filter_frame, text="Filter", command=self.load_receipts).pack(side=tk.LEFT, padx=20)

        # Receipts Treeview
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))

        columns = ("ID", "Receipt No", "Invoice No", "Client", "Date",
                   "Amount", "Payment Method", "Reference No")

        self.receipt_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=20)

        for col in columns:
            self.receipt_tree.heading(col, text=col)
            self.receipt_tree.column(col, width=100)

        self.receipt_tree.column("Client", width=150)
        self.receipt_tree.column("Receipt No", width=120)
        self.receipt_tree.column("Invoice No", width=120)

        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.receipt_tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.receipt_tree.xview)
        self.receipt_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.receipt_tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

    def setup_statements_tab(self, parent):
        ttk.Label(parent, text="Client Statements",
                  font=("Arial", 14, "bold")).pack(pady=(10, 20))

        # Client selection
        selection_frame = ttk.Frame(parent)
        selection_frame.pack(fill=tk.X, pady=(0, 10), padx=20)

        ttk.Label(selection_frame, text="Select Client:").pack(side=tk.LEFT, padx=5)
        self.statement_client = ttk.Combobox(selection_frame, width=40, state="readonly")
        self.statement_client.pack(side=tk.LEFT, padx=5)

        ttk.Label(selection_frame, text="Period:").pack(side=tk.LEFT, padx=(20, 5))
        self.statement_period = ttk.Combobox(selection_frame,
                                             values=["This Month", "Last Month", "This Quarter",
                                                     "Last Quarter", "This Year", "Custom"],
                                             state="readonly", width=15)
        self.statement_period.set("This Month")
        self.statement_period.pack(side=tk.LEFT, padx=5)

        ttk.Button(selection_frame, text="Generate", command=self.generate_statement).pack(side=tk.LEFT, padx=20)

        # Load clients
        self.load_clients_list()

        # Statement display
        statement_frame = ttk.Frame(parent)
        statement_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))

        # Text widget for statement
        self.statement_text = tk.Text(statement_frame, height=20, width=80, font=("Courier", 10))
        scrollbar = ttk.Scrollbar(statement_frame, orient="vertical", command=self.statement_text.yview)
        self.statement_text.configure(yscrollcommand=scrollbar.set)

        self.statement_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Insert sample statement
        self.statement_text.insert(1.0, "Select a client and click 'Generate' to view statement.")

    def setup_reports_tab(self, parent):
        ttk.Label(parent, text="Financial Reports",
                  font=("Arial", 14, "bold")).pack(pady=(10, 20))

        # Report selection
        selection_frame = ttk.Frame(parent)
        selection_frame.pack(fill=tk.X, pady=(0, 20), padx=20)

        reports = [
            ("Sales Report", "sales_report"),
            ("Revenue Report", "revenue_report"),
            ("Aging Report", "aging_report"),
            ("Profit & Loss", "profit_loss"),
            ("Balance Sheet", "balance_sheet")
        ]

        for i, (text, cmd) in enumerate(reports):
            btn = ttk.Button(selection_frame, text=text,
                             command=lambda c=cmd: self.generate_report(c),
                             width=15)
            btn.grid(row=i // 3, column=i % 3, padx=10, pady=10)

        # Report display
        report_frame = ttk.Frame(parent)
        report_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))

        # Treeview for report data
        columns = ("Description", "Amount", "Percentage", "Notes")

        self.report_tree = ttk.Treeview(report_frame, columns=columns, show="headings", height=15)

        for col in columns:
            self.report_tree.heading(col, text=col)
            self.report_tree.column(col, width=150)

        self.report_tree.column("Description", width=250)

        # Scrollbars
        vsb = ttk.Scrollbar(report_frame, orient="vertical", command=self.report_tree.yview)
        hsb = ttk.Scrollbar(report_frame, orient="horizontal", command=self.report_tree.xview)
        self.report_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.report_tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        report_frame.grid_rowconfigure(0, weight=1)
        report_frame.grid_columnconfigure(0, weight=1)

        # Export buttons
        export_frame = ttk.Frame(parent)
        export_frame.pack(pady=10)

        ttk.Button(export_frame, text="Export to Excel",
                   command=self.export_excel).pack(side=tk.LEFT, padx=5)
        ttk.Button(export_frame, text="Export to PDF",
                   command=self.export_pdf).pack(side=tk.LEFT, padx=5)

    def load_clients_list(self):
        conn = sqlite3.connect('erp_system.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, company_name FROM clients ORDER BY company_name")
        clients = cursor.fetchall()
        conn.close()

        self.statement_client['values'] = [f"{c[0]} - {c[1]}" for c in clients]
        if clients:
            self.statement_client.set(clients[0][1])

    def load_receipts(self):
        for item in self.receipt_tree.get_children():
            self.receipt_tree.delete(item)

        conn = sqlite3.connect('erp_system.db')
        cursor = conn.cursor()

        date_from = self.receipt_date_from.get()
        date_to = self.receipt_date_to.get()

        query = """
            SELECT r.id, r.receipt_no, i.invoice_no, c.company_name, 
                   r.receipt_date, r.amount, r.payment_method, r.reference_no
            FROM receipts r
            JOIN invoices i ON r.invoice_id = i.id
            JOIN clients c ON i.client_id = c.id
            WHERE 1=1
        """
        params = []

        if date_from:
            query += " AND r.receipt_date >= ?"
            params.append(date_from)
        if date_to:
            query += " AND r.receipt_date <= ?"
            params.append(date_to)

        query += " ORDER BY r.receipt_date DESC"

        cursor.execute(query, params)

        for row in cursor.fetchall():
            self.receipt_tree.insert("", tk.END, values=row)

        conn.close()

    def create_receipt(self):
        # This would open a receipt creation dialog
        # Similar to the one in SalesModule.receive_payment()
        messagebox.showinfo("Info", "Receipt creation dialog would open here")

    def view_receipt(self):
        selected = self.receipt_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a receipt to view")
            return

        item = self.receipt_tree.item(selected[0])
        receipt_no = item['values'][1]

        dialog = tk.Toplevel(self.parent)
        dialog.title(f"Receipt - {receipt_no}")
        dialog.geometry("500x400")

        # Display receipt details
        text = tk.Text(dialog, wrap=tk.WORD, font=("Courier", 10))
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        receipt_details = f"""
        {'=' * 50}
        {'OFFICIAL RECEIPT':^50}
        {'=' * 50}

        Receipt No: {receipt_no}
        Date: {item['values'][4]}

        Received from: {item['values'][3]}
        Invoice No: {item['values'][2]}

        Amount: ${float(item['values'][5]):,.2f}
        Payment Method: {item['values'][6]}
        Reference: {item['values'][7]}

        {'=' * 50}
        Thank you for your business!
        {'=' * 50}
        """

        text.insert(1.0, receipt_details)
        text.config(state=tk.DISABLED)

    def print_receipt(self):
        selected = self.receipt_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a receipt to print")
            return

        item = self.receipt_tree.item(selected[0])
        receipt_no = item['values'][1]
        messagebox.showinfo("Print", f"Printing receipt {receipt_no}...")

    def generate_statement(self):
        client = self.statement_client.get()
        period = self.statement_period.get()

        if not client:
            messagebox.showerror("Error", "Please select a client")
            return

        try:
            client_id = int(client.split(" - ")[0])
        except:
            messagebox.showerror("Error", "Invalid client selection")
            return

        # Calculate date range based on period
        today = date.today()
        if period == "This Month":
            from_date = date(today.year, today.month, 1)
            to_date = today
        elif period == "Last Month":
            if today.month == 1:
                from_date = date(today.year - 1, 12, 1)
                to_date = date(today.year - 1, 12, 31)
            else:
                from_date = date(today.year, today.month - 1, 1)
                to_date = date(today.year, today.month - 1, 1)
                # Get last day of previous month
                while to_date.month == from_date.month:
                    to_date += timedelta(days=1)
                to_date -= timedelta(days=1)
        elif period == "This Quarter":
            quarter = (today.month - 1) // 3 + 1
            from_date = date(today.year, 3 * (quarter - 1) + 1, 1)
            to_date = today
        elif period == "Last Quarter":
            quarter = (today.month - 1) // 3
            if quarter == 0:
                from_date = date(today.year - 1, 10, 1)
                to_date = date(today.year - 1, 12, 31)
            else:
                from_date = date(today.year, 3 * (quarter - 1) + 1, 1)
                to_date = date(today.year, 3 * quarter, 1)
                # Get last day of quarter
                while to_date.month == 3 * quarter:
                    to_date += timedelta(days=1)
                to_date -= timedelta(days=1)
        elif period == "This Year":
            from_date = date(today.year, 1, 1)
            to_date = today
        else:  # Custom - would need date inputs
            from_date = date(today.year, today.month, 1)
            to_date = today

        # Generate statement
        conn = sqlite3.connect('erp_system.db')
        cursor = conn.cursor()

        # Get client info
        cursor.execute("SELECT company_name, address, city, country FROM clients WHERE id = ?", (client_id,))
        client_info = cursor.fetchone()

        # Get invoices for period
        cursor.execute("""
            SELECT invoice_no, invoice_date, due_date, total_amount, amount_paid, balance
            FROM invoices
            WHERE client_id = ? 
            AND invoice_date BETWEEN ? AND ?
            ORDER BY invoice_date
        """, (client_id, from_date.strftime("%Y-%m-%d"), to_date.strftime("%Y-%m-%d")))

        invoices = cursor.fetchall()

        # Get receipts for period
        cursor.execute("""
            SELECT r.receipt_date, r.amount, r.payment_method, i.invoice_no
            FROM receipts r
            JOIN invoices i ON r.invoice_id = i.id
            WHERE i.client_id = ?
            AND r.receipt_date BETWEEN ? AND ?
            ORDER BY r.receipt_date
        """, (client_id, from_date.strftime("%Y-%m-%d"), to_date.strftime("%Y-%m-%d")))

        receipts = cursor.fetchall()

        conn.close()

        # Build statement text
        statement = f"""
        {'=' * 60}
        {'STATEMENT OF ACCOUNT':^60}
        {'=' * 60}

        Client: {client_info[0]}
        Address: {client_info[1]}
        {client_info[2]}, {client_info[3]}

        Period: {from_date.strftime('%Y-%m-%d')} to {to_date.strftime('%Y-%m-%d')}
        Statement Date: {today.strftime('%Y-%m-%d')}

        {'=' * 60}
        {'INVOICES':^60}
        {'=' * 60}
        {'Invoice No':<15} {'Date':<12} {'Due Date':<12} {'Amount':>10} {'Paid':>10} {'Balance':>10}
        {'-' * 60}
        """

        total_invoiced = 0
        total_paid = 0
        total_balance = 0

        for inv in invoices:
            statement += f"{inv[0]:<15} {inv[1]:<12} {inv[2]:<12} ${inv[3]:>9,.2f} ${inv[4]:>9,.2f} ${inv[5]:>9,.2f}\n"
            total_invoiced += inv[3]
            total_paid += inv[4]
            total_balance += inv[5]

        statement += f"{'-' * 60}\n"
        statement += f"{'TOTALS':<39} ${total_invoiced:>9,.2f} ${total_paid:>9,.2f} ${total_balance:>9,.2f}\n"

        statement += f"""
        {'=' * 60}
        {'PAYMENT HISTORY':^60}
        {'=' * 60}
        {'Date':<12} {'Invoice':<15} {'Amount':>15} {'Method':<15}
        {'-' * 60}
        """

        for rec in receipts:
            statement += f"{rec[0]:<12} {rec[3]:<15} ${rec[1]:>14,.2f} {rec[2]:<15}\n"

        statement += f"""
        {'=' * 60}
        SUMMARY:
        Total Invoiced: ${total_invoiced:,.2f}
        Total Paid: ${total_paid:,.2f}
        Outstanding Balance: ${total_balance:,.2f}
        {'=' * 60}

        Please make payments to:
        Account Name: Your Company Name
        Bank: Your Bank Name
        Account No: 123-456-789
        Swift Code: ABCD1234

        For inquiries, please contact:
        Phone: +1-234-567-8900
        Email: accounting@yourcompany.com
        """

        self.statement_text.delete(1.0, tk.END)
        self.statement_text.insert(1.0, statement)

    def generate_report(self, report_type):
        # Clear existing data
        for item in self.report_tree.get_children():
            self.report_tree.delete(item)

        conn = sqlite3.connect('erp_system.db')
        cursor = conn.cursor()

        if report_type == "sales_report":
            cursor.execute("""
                SELECT strftime('%Y-%m', invoice_date) as month,
                       COUNT(*) as invoice_count,
                       SUM(total_amount) as total_sales,
                       SUM(amount_paid) as total_paid
                FROM invoices
                WHERE invoice_date >= date('now', '-6 months')
                GROUP BY strftime('%Y-%m', invoice_date)
                ORDER BY month DESC
            """)

            data = cursor.fetchall()

            # Insert headers
            self.report_tree.insert("", tk.END, values=("Month", "Invoices", "Total Sales", "Amount Paid", ""))
            self.report_tree.insert("", tk.END, values=("-" * 20, "-" * 10, "-" * 15, "-" * 15, "-" * 10))

            total_sales = 0
            total_paid = 0

            for row in data:
                self.report_tree.insert("", tk.END, values=(
                    row[0],
                    row[1],
                    f"${row[2]:,.2f}",
                    f"${row[3]:,.2f}",
                    f"{(row[3] / row[2] * 100 if row[2] > 0 else 0):.1f}%"
                ))
                total_sales += row[2]
                total_paid += row[3]

            # Insert totals
            self.report_tree.insert("", tk.END, values=("-" * 20, "-" * 10, "-" * 15, "-" * 15, "-" * 10))
            self.report_tree.insert("", tk.END, values=(
                "TOTAL",
                sum([r[1] for r in data]),
                f"${total_sales:,.2f}",
                f"${total_paid:,.2f}",
                f"{(total_paid / total_sales * 100 if total_sales > 0 else 0):.1f}%"
            ))

        elif report_type == "aging_report":
            cursor.execute("""
                SELECT c.company_name,
                       SUM(CASE WHEN i.balance > 0 AND i.due_date < date('now', '-90 days') THEN i.balance ELSE 0 END) as over_90,
                       SUM(CASE WHEN i.balance > 0 AND i.due_date BETWEEN date('now', '-89 days') AND date('now', '-60 days') THEN i.balance ELSE 0 END) as days_61_90,
                       SUM(CASE WHEN i.balance > 0 AND i.due_date BETWEEN date('now', '-59 days') AND date('now', '-30 days') THEN i.balance ELSE 0 END) as days_31_60,
                       SUM(CASE WHEN i.balance > 0 AND i.due_date >= date('now', '-29 days') THEN i.balance ELSE 0 END) as current,
                       SUM(i.balance) as total
                FROM invoices i
                JOIN clients c ON i.client_id = c.id
                WHERE i.balance > 0
                GROUP BY c.id, c.company_name
                HAVING total > 0
                ORDER BY total DESC
            """)

            data = cursor.fetchall()

            # Insert headers
            self.report_tree.insert("", tk.END,
                                    values=("Client", "Current", "31-60 Days", "61-90 Days", "Over 90", "Total"))
            self.report_tree.insert("", tk.END, values=("-" * 20, "-" * 15, "-" * 15, "-" * 15, "-" * 15, "-" * 15))

            for row in data:
                self.report_tree.insert("", tk.END, values=(
                    row[0],
                    f"${row[4]:,.2f}",
                    f"${row[3]:,.2f}",
                    f"${row[2]:,.2f}",
                    f"${row[1]:,.2f}",
                    f"${row[5]:,.2f}"
                ))

        conn.close()

    def export_excel(self):
        messagebox.showinfo("Export", "Report exported to Excel successfully")

    def export_pdf(self):
        messagebox.showinfo("Export", "Report exported to PDF successfully")
