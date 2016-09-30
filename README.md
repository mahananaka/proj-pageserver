# README #

A "getting started" project for CIS 322, software engineering 1 at University of Oregon.

### What is this repository for? ###

* This project is a first step for myself as a CIS 322 student to get:
  * Initial experience with GIT workflow:  Fork the project, make and test changes locally, commit;  turn in repository URL
  * Initial experience with automated configuration for turnkey installation
  * Extend a tiny web server in Python, to check understanding of basic web architecture
  * Use automated tests to check progress (plus manual tests for good measure)

### What do I need?  Where will it work? ###

* Designed for Unix, mostly interoperable on Linux (Ubuntu) or MacOS.
  Target environment is Raspberry Pi. 
  ** May also work on Windows, but no promises.  A Linux virtual machine
   may work, but our experience has not been good; if you don't have a 
   Raspberry Pi in hand yet, you may want to test on shared server ix. 
* You will need Python version 3.4 or higher. 
* Designed to work in "user mode" (unprivileged), therefore using a port 
  number above 1000 (rather than port 80 that a privileged web server would use)

### Assignment ###
*What will this tiny web server do?
  *This server will except http requests over an unpriveledged port.
  *It will route requests to the desired page if it exists within a default directory.
  *If the URL contains potentially dangerous character sequences it will return a 403 Forbidden page.
  *If the file requested could not be found it will return a 404 error.
  ### Author: Jared Paeschke , jpaeschk@uoregon.edu ###
