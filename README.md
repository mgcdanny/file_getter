Folder Structure:


Folder | Subfolder | Files
---- | ---- | ----
Modified_File_Getter | | 
	| fileCrawler.py (main script to be executed) |
	| files_all | 
		| most recent copy of all files |
 	| config |
 		| search_these_directories.txt |
 		| skip_these_directories.txt |
 		| skip_these_files.txt |
 	| files_update |
 		| folder_date1 |
 			| most recent copy as of date1 |
 		| folder_date2 |
 			| most recent copy as of date2 |
 		| folder_dateX |
 			| most recent copy as of dateX |
	| last_run_time |
		| LAST_RUN.txt (persists the last completed run time) |
	| logs |
		| file_date1 (log for date1 run) |
		| file_date2 (log for date2 run) |
    	| file_dateX (log for dateX run) |
    | readme |
    	| readme.txt (this file) |


Notes:
This program was developed to help maintain a central location of the most recent version of files saved across sprawling directory structures.

This program crawls through the file directory and checks various "requirments".  If those requirments are met, two copies of the file are made and saved in a "central location."  

The "requriments" are as follows:
	The file is contained in a directory designated in search_these_directories.txt
	The file has the designated extension in fileCrawler.py in variable FILE_TYPE
	The file has a modified date greater than the value in LAST_RUN.txt
	The file is not designated in skip_these_files.txt
	The file is not in a directory designated in skip_these_directories.txt

The "central location," where files are copied to, consists of two directories:
	1) THIS IS DISABLED: The files_all directory, which is all the files.  When a modified file is found by the program a copy will be saved here.  If a filename already exists in this directory, it will be overwritten here. Thus keeping only the most up-to-date version. 
	
	2) The files_update directory has sub-directories which are created at run time for each execution of the program.  The subfolder names are the datetime stamp of execution.  Inside these subfolders are a copy of only the modified files found during that execution.  This is known as the 'delta,' and helps keep track of only which files have been modified since that last execution.

Deleting stuff:
	The .log files can be deleted and are primarly used to learn what the program is doing.  These will be helpful to debug issues.
	The subdirectories containg the 'delta' files can be deleted.
	The files in the files_all directory can be deleted.

DO NOT DELETE the following:
	
	The "files_all", "files_serach", "files_update", "last_run_time", "logs" directories themselves.
	The "LAST_RUN.txt" must exist and contain a value like YYYY-MM-DD-HH-MM-SS. For example: 2014-04-25-12-20-05.
	These files must exist and contain valid formatting:
		"search_these_directories.txt"
		"skip_these_directories.txt"
		"skip_these_files.txt"
	Valid directory formatting is:
		C:/Users/dgabrieli/Desktop/tester
	Valid file formatting is:
		C:/Users/dgabrieli/Desktop/tester/skip_me.txt


