import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import datetime

class Book:
    """Class to represent a single book or a book series."""
    def __init__(self, book_id, title, author, volumes=None):
        self.id = book_id
        self.title = title
        self.author = author
        
        # Series handling
        self.volumes = volumes if volumes else []
        self.is_series = len(self.volumes) > 0
        self.series_status = {} # Map: volume_name -> {'checkout': date, 'due': date}

        # Single book state
        self.is_checked_out = False
        self.checkout_date = None
        self.due_date = None
        self.days_borrowed = 0

    def get_status_display(self):
        """Returns the status string for the table."""
        if self.is_series:
            borrowed_count = len(self.series_status)
            total_count = len(self.volumes)
            if borrowed_count == 0:
                return "Available"
            elif borrowed_count == total_count:
                return "All Checked Out"
            else:
                return f"{borrowed_count}/{total_count} Checked Out"
        else:
            return "Checked Out" if self.is_checked_out else "Available"

    def get_available_volumes(self):
        """Returns a list of volumes that are NOT checked out."""
        if not self.is_series:
            return []
        return [v for v in self.volumes if v not in self.series_status]

    def get_borrowed_volumes(self):
        """Returns a list of volumes that ARE checked out."""
        if not self.is_series:
            return []
        return list(self.series_status.keys())

    def check_out(self, days, volume_name=None):
        now = datetime.datetime.now()
        due = now + datetime.timedelta(days=days)

        if self.is_series and volume_name:
            self.series_status[volume_name] = {'checkout': now, 'due': due}
        else:
            self.is_checked_out = True
            self.days_borrowed = days
            self.checkout_date = now
            self.due_date = due

    def return_book(self, volume_name=None):
        if self.is_series and volume_name:
            if volume_name in self.series_status:
                del self.series_status[volume_name]
        else:
            self.is_checked_out = False
            self.checkout_date = None
            self.due_date = None
            self.days_borrowed = 0

class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Book Sorter & Tracker")
        self.root.geometry("1100x650")
        self.root.configure(bg="#f4f6f7")  # Soft gray background

        # --- Modern Styling ---
        self.style = ttk.Style()
        self.style.theme_use('clam')  # 'clam' provides a good base for custom coloring

        # Colors
        bg_color = "#f4f6f7"
        header_bg = "#2c3e50"  # Dark blue-gray
        header_fg = "white"
        select_bg = "#3498db"  # Bright blue
        
        # Configure Treeview (The Table)
        self.style.configure("Treeview", 
                             background="white",
                             foreground="#2c3e50",
                             rowheight=30,
                             fieldbackground="white",
                             font=("Segoe UI", 10))
        
        self.style.configure("Treeview.Heading", 
                             background=header_bg,
                             foreground=header_fg,
                             font=("Segoe UI", 10, "bold"),
                             relief="flat")
        
        self.style.map("Treeview", 
                       background=[('selected', select_bg)])
        
        # Configure Buttons
        self.style.configure("TButton", 
                             font=("Segoe UI", 10), 
                             padding=6,
                             background="#ecf0f1")
        
        self.style.map("TButton",
                       background=[('active', '#bdc3c7')]) 

        # Initialize the list of books
        self.books = []
        self.initialize_books()

        # Build the UI
        self.create_widgets()
        self.refresh_table()

    def initialize_books(self):
        """Pre-populates the library with books and series."""
        # Standard Single Books
        initial_data = [
            ("The Great Gatsby", "F. Scott Fitzgerald"),
            ("1984", "George Orwell"),
            ("To Kill a Mockingbird", "Harper Lee"),
            ("Pride and Prejudice", "Jane Austen"),
            ("The Catcher in the Rye", "J.D. Salinger"),
            ("The Hobbit", "J.R.R. Tolkien"),
            ("Fahrenheit 451", "Ray Bradbury"),
            ("Moby Dick", "Herman Melville"),
            ("War and Peace", "Leo Tolstoy"),
            ("The Odyssey", "Homer"),
            ("Ulysses", "James Joyce"),
            ("Madame Bovary", "Gustave Flaubert"),
            ("The Divine Comedy", "Dante Alighieri"),
            ("The Brothers Karamazov", "Fyodor Dostoevsky"),
            ("Don Quixote", "Miguel de Cervantes")
        ]
        
        for i, (title, author) in enumerate(initial_data, 1):
            self.books.append(Book(i, title, author))

        # Add Series
        hp_volumes = [
            "1. The Sorcerer's Stone", "2. The Chamber of Secrets", "3. The Prisoner of Azkaban",
            "4. The Goblet of Fire", "5. The Order of the Phoenix", "6. The Half-Blood Prince",
            "7. The Deathly Hallows"
        ]
        self.books.append(Book(16, "Harry Potter (Series)", "J.K. Rowling", volumes=hp_volumes))

        lotr_volumes = [
            "1. The Fellowship of the Ring", "2. The Two Towers", "3. The Return of the King"
        ]
        self.books.append(Book(17, "The Lord of the Rings (Series)", "J.R.R. Tolkien", volumes=lotr_volumes))


    def create_widgets(self):
        # Main Container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Top Header ---
        header_frame = tk.Frame(main_frame, bg="#f4f6f7")
        header_frame.pack(fill=tk.X, pady=(0, 15))

        title_lbl = tk.Label(header_frame, text="Library Management System", 
                             font=("Segoe UI", 24, "bold"), 
                             bg="#f4f6f7", fg="#2c3e50")
        title_lbl.pack(side=tk.LEFT)

        # --- Control Panel (Action Bar) ---
        # Using a LabelFrame for visual grouping
        controls = tk.LabelFrame(main_frame, text="Controls", 
                                 font=("Segoe UI", 11, "bold"),
                                 bg="#f4f6f7", fg="#7f8c8d",
                                 padx=15, pady=15, relief="flat", bd=1)
        controls.pack(fill=tk.X, pady=(0, 15))

        # Action Buttons
        ttk.Button(controls, text="Check Out Book", command=self.action_checkout).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(controls, text="Return Book", command=self.action_return).pack(side=tk.LEFT, padx=(0, 10))
        
        # Vertical Separator
        ttk.Separator(controls, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=15)

        # Sorting Buttons
        tk.Label(controls, text="Sort by:", bg="#f4f6f7", font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(controls, text="Title", command=lambda: self.sort_books("title")).pack(side=tk.LEFT, padx=2)
        ttk.Button(controls, text="Author", command=lambda: self.sort_books("author")).pack(side=tk.LEFT, padx=2)
        ttk.Button(controls, text="Status", command=lambda: self.sort_books("status")).pack(side=tk.LEFT, padx=2)

        # --- Treeview (Table) ---
        table_frame = ttk.Frame(main_frame)
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("ID", "Title", "Author", "Status", "Checkout Date", "Due Date")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")

        # Define Headings
        for col in columns:
            self.tree.heading(col, text=col)

        # Define Columns Width
        self.tree.column("ID", width=50, anchor=tk.CENTER)
        self.tree.column("Title", width=250)
        self.tree.column("Author", width=200)
        self.tree.column("Status", width=150, anchor=tk.CENTER)
        self.tree.column("Checkout Date", width=160, anchor=tk.CENTER)
        self.tree.column("Due Date", width=160, anchor=tk.CENTER)

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Tag configuration for colors
        self.tree.tag_configure("oddrow", background="white")
        self.tree.tag_configure("evenrow", background="#e8f6f3") 
        
        self.tree.tag_configure("checked_out_text", foreground="#c0392b", font=("Segoe UI", 10, "bold")) 
        self.tree.tag_configure("available_text", foreground="#27ae60", font=("Segoe UI", 10, "bold"))
        self.tree.tag_configure("partial_text", foreground="#d35400", font=("Segoe UI", 10, "bold")) # Orange for partial series

    def refresh_table(self):
        """Clears the table and repopulates it with current book data."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        for i, book in enumerate(self.books):
            # Status Logic
            status_text = book.get_status_display()
            
            # Date Logic
            checkout_str = "-"
            due_str = "-"
            
            if book.is_series:
                if book.series_status:
                     # For series, just show "Various" if multiple, or the date if 1
                     if len(book.series_status) == 1:
                         # Get the only item's dates
                         val = list(book.series_status.values())[0]
                         checkout_str = val['checkout'].strftime("%Y-%m-%d")
                         due_str = val['due'].strftime("%Y-%m-%d")
                     else:
                         checkout_str = "Various"
                         due_str = "Various"
            else:
                checkout_str = book.checkout_date.strftime("%Y-%m-%d %H:%M") if book.checkout_date else "-"
                due_str = book.due_date.strftime("%Y-%m-%d %H:%M") if book.due_date else "-"

            # Visual Tags
            row_tag = "evenrow" if i % 2 == 0 else "oddrow"
            
            if "Available" in status_text:
                status_tag = "available_text"
            elif "All" in status_text or (not book.is_series and book.is_checked_out):
                status_tag = "checked_out_text"
            else:
                status_tag = "partial_text"

            self.tree.insert("", tk.END, values=(
                book.id,
                book.title,
                book.author,
                status_text,
                checkout_str,
                due_str
            ), tags=(row_tag, status_tag))

    def get_selected_book(self):
        """Returns the Book object associated with the selected row."""
        selected_item = self.tree.selection()
        if not selected_item:
            return None
        
        item_values = self.tree.item(selected_item)['values']
        book_id = item_values[0]

        for book in self.books:
            if book.id == book_id:
                return book
        return None

    def ask_selection(self, title, prompt, options):
        """Custom dialog to select an option from a dropdown."""
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("300x150")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text=prompt, padx=10, pady=10).pack()

        choice_var = tk.StringVar()
        combobox = ttk.Combobox(dialog, textvariable=choice_var, values=options, state="readonly")
        combobox.pack(padx=10, pady=5)
        combobox.current(0)

        self.selected_choice = None
        def on_ok():
            self.selected_choice = choice_var.get()
            dialog.destroy()

        ttk.Button(dialog, text="OK", command=on_ok).pack(pady=10)
        self.root.wait_window(dialog)
        return self.selected_choice

    def action_checkout(self):
        book = self.get_selected_book()
        if not book:
            messagebox.showwarning("Selection Error", "Please select a book to check out.")
            return

        volume_to_checkout = None

        # Series Logic
        if book.is_series:
            available_vols = book.get_available_volumes()
            if not available_vols:
                messagebox.showerror("Unavailable", "All books in this series are currently checked out.")
                return
            
            # Ask user which volume
            volume_to_checkout = self.ask_selection("Select Volume", f"Which book from '{book.title}'?", available_vols)
            if not volume_to_checkout:
                return # User cancelled
        
        # Single Book Logic
        elif book.is_checked_out:
            messagebox.showerror("Unavailable", f"'{book.title}' is already checked out.")
            return

        # Common Duration Input
        days = simpledialog.askinteger("Input", f"How many days to borrow?", minvalue=1, maxvalue=365)
        
        if days:
            book.check_out(days, volume_to_checkout)
            self.refresh_table()
            msg_title = volume_to_checkout if volume_to_checkout else book.title
            messagebox.showinfo("Success", f"You have checked out '{msg_title}' for {days} days.")

    def action_return(self):
        book = self.get_selected_book()
        if not book:
            messagebox.showwarning("Selection Error", "Please select a book to return.")
            return

        volume_to_return = None

        # Series Logic
        if book.is_series:
            borrowed_vols = book.get_borrowed_volumes()
            if not borrowed_vols:
                messagebox.showinfo("Info", "No books from this series are currently borrowed.")
                return
            
            volume_to_return = self.ask_selection("Return Volume", f"Which book to return from '{book.title}'?", borrowed_vols)
            if not volume_to_return:
                return
            
        # Single Book Logic
        elif not book.is_checked_out:
            messagebox.showinfo("Info", f"'{book.title}' is already in the library.")
            return

        display_name = volume_to_return if volume_to_return else book.title

        if messagebox.askyesno("Confirm Return", f"Return '{display_name}'?"):
            book.return_book(volume_to_return)
            self.refresh_table()

    def sort_books(self, criteria):
        """Sorts the book list based on criteria."""
        if criteria == "title":
            self.books.sort(key=lambda x: x.title)
        elif criteria == "author":
            self.books.sort(key=lambda x: x.author)
        elif criteria == "status":
            # Sort logic: Available < Partial < Checked Out
            self.books.sort(key=lambda x: x.get_status_display())
        
        self.refresh_table()

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()