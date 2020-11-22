# Virtual Memory Simulation using python

## Overview

* Virtual memory allows a process of P pages to run in F frames, even if F < P. This is achieved by use of a page table, which records which pages are in RAM in which frames, and a page fault mechanism by which the memory management unit (MMU) can ask the operating system (OS) to bring in a page from disk. 

## Goals
* Simulate working of the OS to maintain a process' use of RAM and the page table.
* The page table must be accessible by MMU and OS


## Specifications

The page table has four fields in each page table entry:
* Valid indicating if the page of that index is in RAM.
* Frame giving the frame number of the page in RAM.
* Dirty indicating if the page has been written to.
* Requested which is non-zero only if that page is not in RAM and has been requested by the MMU. In this case it's value is the PID of the MMU.
* Added a fifth attribute in the page table to keep track of the count of page access for finding the victim page using LRU algorithm.

MMU simulator takes several arguments as input

* No. of pages in process
* Reference string 
* PID of the OS Process

Example : 
* 5,"R0 R1 R1 W3 R0 R2 R2 W4 R0 R2 R2 W4 R0 R2 R2 W4 R0 R1 R1 W3 R0 R1 R1 W3", 10,

OS simulator takes two parameters as input:

* No. of pages in process
* No. of frames allocated to the process

Example: 
* (5,3,)

* Os simulator uses least recently used (LRU) algorithm for selecting the victim page



## Algorithm

* The Simulator uses threads to run both OS and MMU simultaneously to make the simulation more realistic.

Memory management unit
* Checks if the page is in RAM.
* If not in RAM, writes its PID into the Requested field for that page.
* Simulates a page fault by signalling the OS with a SIGUSR1.
* Blocks until it receives a SIGCONT signal from the OS to indicate that the page has been loaded (load is not done in this project, just simulated by sleep(1) delays).
* If the access is a write access, set the Dirty bit.
* Print the updated page table.

Operating System
* Scan through the page table looking for a non-zero value in the Requested field.
* If a non-zero value is found, it's the PID of the MMU, and indicates that the MMU wants the page at that index loaded.
* If there is a free frame allocate the next one to the page.
* If there are no free frames, we choose the least recently used page as the victim page
* If the victim page is dirty, simulate writing the page to disk by sleep(1) and increment the counter of disk accesses.
* Update the page table to indicate that the victim page is no longer Valid.
* Simulate the page load by sleep(1) and increment the counter of disk accesses.
* Update the page table to indicate that the page is Valid, in the allocated Frame, not Dirty, and clear the Requested field.
* Print the updated page table.
* Send a SIGCONT signal to the MMU to indicate that the page is now loaded.
* If no non-zero Requested field was found, the OS exits the loop.


