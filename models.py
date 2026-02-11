from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional, List


@dataclass
class Client:
    id: Optional[int] = None
    client_code: str = ""
    company_name: str = ""
    contact_person: str = ""
    email: str = ""
    phone: str = ""
    address: str = ""
    city: str = ""
    country: str = ""
    tax_id: str = ""
    credit_limit: float = 0.0
    payment_terms: str = ""
    status: str = "Active"
    created_date: Optional[datetime] = None
    notes: str = ""


@dataclass
class Supplier:
    id: Optional[int] = None
    supplier_code: str = ""
    company_name: str = ""
    contact_person: str = ""
    email: str = ""
    phone: str = ""
    address: str = ""
    city: str = ""
    country: str = ""
    tax_id: str = ""
    lead_time_days: int = 7
    payment_terms: str = ""
    status: str = "Active"
    created_date: Optional[datetime] = None
    notes: str = ""


@dataclass
class Product:
    id: Optional[int] = None
    product_code: str = ""
    product_name: str = ""
    description: str = ""
    category: str = ""
    unit: str = ""
    unit_price: float = 0.0
    cost_price: float = 0.0
    min_stock_level: int = 10
    max_stock_level: int = 100
    current_stock: int = 0
    supplier_id: Optional[int] = None
    reorder_point: int = 20
    status: str = "Active"
    created_date: Optional[datetime] = None


@dataclass
class Quotation:
    id: Optional[int] = None
    quotation_no: str = ""
    client_id: int = 0
    date: date = date.today()
    valid_until: date = date.today()
    status: str = "Draft"
    subtotal: float = 0.0
    tax_rate: float = 0.0
    tax_amount: float = 0.0
    total_amount: float = 0.0
    notes: str = ""
    terms_conditions: str = ""
    created_by: str = ""
    created_date: Optional[datetime] = None
    items: List = None

    def __post_init__(self):
        if self.items is None:
            self.items = []


@dataclass
class SalesOrder:
    id: Optional[int] = None
    order_no: str = ""
    quotation_id: Optional[int] = None
    client_id: int = 0
    order_date: date = date.today()
    delivery_date: date = date.today()
    status: str = "Pending"
    subtotal: float = 0.0
    tax_amount: float = 0.0
    total_amount: float = 0.0
    payment_status: str = "Unpaid"
    notes: str = ""
    created_by: str = ""
    created_date: Optional[datetime] = None
    items: List = None

    def __post_init__(self):
        if self.items is None:
            self.items = []


@dataclass
class PurchaseOrder:
    id: Optional[int] = None
    po_no: str = ""
    supplier_id: int = 0
    order_date: date = date.today()
    expected_delivery: date = date.today()
    status: str = "Pending"
    subtotal: float = 0.0
    tax_amount: float = 0.0
    total_amount: float = 0.0
    confirmation_date: Optional[date] = None
    confirmed_by: str = ""
    notes: str = ""
    created_by: str = ""
    created_date: Optional[datetime] = None
    items: List = None

    def __post_init__(self):
        if self.items is None:
            self.items = []


@dataclass
class Invoice:
    id: Optional[int] = None
    invoice_no: str = ""
    order_id: int = 0
    client_id: int = 0
    invoice_date: date = date.today()
    due_date: date = date.today()
    subtotal: float = 0.0
    tax_amount: float = 0.0
    total_amount: float = 0.0
    amount_paid: float = 0.0
    balance: float = 0.0
    payment_status: str = "Unpaid"
    notes: str = ""
    created_date: Optional[datetime] = None
