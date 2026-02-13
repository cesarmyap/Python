import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime


class ClientsModule:
    def __init__(self, parent):
        self.parent = parent
        self.setup_ui()
        self.load_clients()

    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Title
        ttk.Label(main_frame, text="Clients Management",
                  font=("Arial", 16, "bold")).pack(pady=(0, 20))

        # Control buttons frame
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Button(control_frame, text="➕ Add New Client",
                   command=self.add_client, style="Success.TButton").pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="✏️ Edit Client",
                   command=self.edit_client).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="🗑️ Delete Client",
                   command=self.delete_client, style="Danger.TButton").pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="🔄 Refresh",
                   command=self.load_clients).pack(side=tk.LEFT, padx=2)

        # Search frame
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Search",
                   command=self.search_clients).pack(side=tk.LEFT, padx=5)

        # Clients Treeview
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("ID", "Client Code", "Company Name", "Contact Person",
                   "Phone", "Email", "City", "Status", "Credit Limit")

        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)

        # Define headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        # Adjust column widths
        self.tree.column("Company Name", width=200)
        self.tree.column("Contact Person", width=150)
        self.tree.column("Email", width=200)

        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Double click to edit
        self.tree.bind("<Double-1>", lambda e: self.edit_client())

    def load_clients(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Load from database
        conn = sqlite3.connect('erp_system.db')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, client_code, company_name, contact_person, phone, email, city, status, credit_limit FROM clients ORDER BY company_name")

        for row in cursor.fetchall():
            self.tree.insert("", tk.END, values=row)

        conn.close()

    def search_clients(self):
        search_term = self.search_var.get().strip()

        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = sqlite3.connect('erp_system.db')
        cursor = conn.cursor()

        if search_term:
            cursor.execute("""
                SELECT id, client_code, company_name, contact_person, phone, email, city, status, credit_limit 
                FROM clients 
                WHERE company_name LIKE ? OR contact_person LIKE ? OR email LIKE ? OR phone LIKE ?
                ORDER BY company_name
            """, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
        else:
            cursor.execute(
                "SELECT id, client_code, company_name, contact_person, phone, email, city, status, credit_limit FROM clients ORDER BY company_name")

        for row in cursor.fetchall():
            self.tree.insert("", tk.END, values=row)

        conn.close()

    def add_client(self):
        self.show_client_dialog()

    def edit_client(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a client to edit")
            return

        item = self.tree.item(selected[0])
        client_id = item['values'][0]

        conn = sqlite3.connect('erp_system.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
        client_data = cursor.fetchone()
        conn.close()

        if client_data:
            self.show_client_dialog(client_data)

    def delete_client(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a client to delete")
            return

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this client?"):
            item = self.tree.item(selected[0])
            client_id = item['values'][0]

            conn = sqlite3.connect('erp_system.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM clients WHERE id = ?", (client_id,))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Client deleted successfully")
            self.load_clients()

    def show_client_dialog(self, client_data=None):
        dialog = tk.Toplevel(self.parent)
        dialog.title("Add/Edit Client" if client_data else "Add Client")
        dialog.geometry("600x500")
        dialog.transient(self.parent)
        dialog.grab_set()

        # Create form
        form_frame = ttk.Frame(dialog, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)

        entries = {}
        row = 0

        fields = [
            ("client_code", "Client Code:", 0, 0),
            ("company_name", "Company Name*:", 0, 1),
            ("contact_person", "Contact Person:", 1, 0),
            ("email", "Email:", 1, 1),
            ("phone", "Phone:", 2, 0),
            ("tax_id", "Tax ID:", 2, 1),
            ("address", "Address:", 3, 0),
            ("city", "City:", 3, 1),
            ("country", "Country:", 4, 0),
            ("credit_limit", "Credit Limit:", 4, 1),
            ("payment_terms", "Payment Terms:", 5, 0),
            ("status", "Status:", 5, 1),
            ("notes", "Notes:", 6, 0)
        ]

        for field_name, label_text, grid_row, grid_col in fields:
            ttk.Label(form_frame, text=label_text).grid(row=grid_row * 2, column=grid_col, sticky=tk.W, pady=(10, 5))

            if field_name == "status":
                entry = ttk.Combobox(form_frame, values=["Active", "Inactive", "Suspended"], state="readonly")
            elif field_name == "notes":
                entry = tk.Text(form_frame, height=4, width=40)
            else:
                entry = ttk.Entry(form_frame, width=30)

            entry.grid(row=grid_row * 2 + 1, column=grid_col, sticky=tk.W + tk.E, padx=(0, 20))
            entries[field_name] = entry

            form_frame.grid_columnconfigure(grid_col, weight=1)

        # Fill form if editing
        if client_data:
            field_names = ["id", "client_code", "company_name", "contact_person", "email", "phone",
                           "address", "city", "country", "tax_id", "credit_limit", "payment_terms",
                           "status", "created_date", "notes"]

            for i, field_name in enumerate(field_names):
                if field_name in entries:
                    if field_name == "notes" and isinstance(entries[field_name], tk.Text):
                        entries[field_name].delete(1.0, tk.END)
                        entries[field_name].insert(1.0, client_data[i] or "")
                    else:
                        entries[field_name].delete(0, tk.END)
                        entries[field_name].insert(0, str(client_data[i] or ""))

        # Buttons frame
        buttons_frame = ttk.Frame(form_frame)
        buttons_frame.grid(row=14, column=0, columnspan=2, pady=20)

        ttk.Button(buttons_frame, text="Save",
                   command=lambda: self.save_client(entries, dialog, client_data),
                   style="Success.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Cancel",
                   command=dialog.destroy).pack(side=tk.LEFT, padx=5)

    def save_client(self, entries, dialog, client_data=None):
        # Validate required fields
        if not entries["company_name"].get().strip():
            messagebox.showerror("Error", "Company Name is required")
            return

        conn = sqlite3.connect('erp_system.db')
        cursor = conn.cursor()

        try:
            if client_data:  # Update existing client
                cursor.execute("""
                    UPDATE clients SET
                    client_code = ?, company_name = ?, contact_person = ?, email = ?,
                    phone = ?, address = ?, city = ?, country = ?, tax_id = ?,
                    credit_limit = ?, payment_terms = ?, status = ?, notes = ?
                    WHERE id = ?
                """, (
                    entries["client_code"].get(),
                    entries["company_name"].get(),
                    entries["contact_person"].get(),
                    entries["email"].get(),
                    entries["phone"].get(),
                    entries["address"].get(),
                    entries["city"].get(),
                    entries["country"].get(),
                    entries["tax_id"].get(),
                    float(entries["credit_limit"].get() or 0),
                    entries["payment_terms"].get(),
                    entries["status"].get(),
                    entries["notes"].get("1.0", tk.END).strip() if isinstance(entries["notes"], tk.Text) else entries[
                        "notes"].get(),
                    client_data[0]
                ))
            else:  # Insert new client
                cursor.execute("""
                    INSERT INTO clients 
                    (client_code, company_name, contact_person, email, phone, 
                     address, city, country, tax_id, credit_limit, payment_terms, status, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    entries["client_code"].get(),
                    entries["company_name"].get(),
                    entries["contact_person"].get(),
                    entries["email"].get(),
                    entries["phone"].get(),
                    entries["address"].get(),
                    entries["city"].get(),
                    entries["country"].get(),
                    entries["tax_id"].get(),
                    float(entries["credit_limit"].get() or 0),
                    entries["payment_terms"].get(),
                    entries["status"].get(),
                    entries["notes"].get("1.0", tk.END).strip() if isinstance(entries["notes"], tk.Text) else entries[
                        "notes"].get()
                ))

            conn.commit()
            messagebox.showinfo("Success", "Client saved successfully")
            dialog.destroy()
            self.load_clients()

        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Client code already exists")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving client: {str(e)}")
        finally:
            conn.close()
