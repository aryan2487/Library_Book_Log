# **Project Statement: Library Book Sorter**

## **Problem Statement**

In small libraries, personal collections, or classroom reading corners, managing books manually is prone to error. Simple logbooks fail to capture the complexity of **Book Series**, where a single entry (e.g., "The Lord of the Rings") actually consists of multiple physical items that need to be tracked individually. There is a need for a digital solution that can handle both standalone titles and multi-volume collections seamlessly, tracking availability and due dates without the overhead of enterprise software.

## **Scope of the Project**

The project is a **Desktop GUI Application** that focuses on the core essentials of library management:

* **Inventory:** Manages a pre-defined set of classic literature titles and major book series.  
* **Granular Tracking:** detailed tracking for individual volumes within a series.  
* **Operations:** Covers the full lifecycle: Checking out specific volumes, calculating dates, viewing partial status, and returning items.

## **Target Users**

* **Small Library Administrators:** Individuals managing classroom or community libraries with mixed collections (singles and series).  
* **Personal Collectors:** Hobbyists who lend books to friends and need to track specific volumes.  
* **Students:** Users learning Object Oriented Design (handling polymorphism between 'Book' and 'Series').

## **High-Level Features**

1. **Series Volume Tracking:** Ability to manage multiple volumes under a single Series title.  
2. **Status Visualization:** Color-coded rows distinguishing between Available, Fully Checked Out, and Partially Checked Out items.  
3. **Smart Selection Dialogs:** Context-aware popups that let users choose specific volumes to borrow or return.  
4. **Automated Date Logic:** Inputting a duration automatically generates exact timestamps for records.