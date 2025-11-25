# **Library Book Sorter & Tracker**

## **Overview**

The **Library Book Sorter & Tracker** is a Python-based GUI application designed to manage a small library collection. It tracks the availability of books, manages check-outs and returns, and calculates due dates. Notably, it includes advanced support for **Book Series**, allowing users to track individual volumes within a collection (e.g., specific *Harry Potter* books) independently.

## **Features**

* **Visual Dashboard:** View 15+ classic books and series with clear status indicators.  
  * 🟢 **Green:** Available  
  * 🔴 **Red:** Checked Out  
  * 🟠 **Orange:** Partially Checked Out (for series)  
* **Series Support:** Intelligent handling of multi-volume series. You can check out "Volume 2" while "Volume 1" remains available.  
* **Check-Out System:** Borrow books by specifying a loan duration. The system automatically records timestamps and due dates.  
* **Return System:** Returns specific volumes or single books to the inventory.  
* **Sorting:** Instantly sort the library catalog by Title, Author, or Status.

## **Technologies Used**

* **Programming Language:** Python 3.x  
* **GUI Framework:** Tkinter (Standard Python GUI library)  
* **Libraries:** tkinter.ttk, datetime

## **Installation & Execution**

### **Prerequisites**

* Ensure **Python 3.x** is installed on your system.

### **Steps to Run**

1. **Clone the repository:**  
   git clone \<your-repo-url\>  
   cd \<your-repo-folder\>

2. **Run the application:**  
   python library\_sorter.py

## **Instructions for Testing**

### **Test 1: Single Book Checkout**

1. Launch the app.  
2. Select "1984" and click **Check Out Book**.  
3. Enter 7 days.  
4. **Result:** Row turns Red, status becomes "Checked Out".

### **Test 2: Series Volume Checkout**

1. Select "Harry Potter (Series)".  
2. Click **Check Out Book**.  
3. A popup appears. Select **"2. The Chamber of Secrets"** and click OK.  
4. Enter 14 days.  
5. **Result:** Row turns Orange, status becomes "1/7 Checked Out", date shows "Various" (if mixed) or the specific date.

### **Test 3: Preventing Double Booking**

1. Select "Harry Potter" (already partially checked out).  
2. Click **Check Out Book** again.  
3. **Result:** The dropdown list **should not** show "2. The Chamber of Secrets" (since it is already out).

### **Test 4: Returning a Volume**

1. Select "Harry Potter".  
2. Click **Return Book**.  
3. Select **"2. The Chamber of Secrets"**.  
4. **Result:** Row turns Green (if no other vols are out), status becomes "Available".



