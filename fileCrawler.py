import os
import shutil
import logging
import datetime as dt


def time_read(fpath, fmt):
    """get time of last run"""
    with open(fpath, 'rb') as f:
        time_previous = f.read()
        return dt.datetime.strptime(time_previous,fmt)

def time_write(fpath, time):
    """write start time of current run"""
    with open(fpath, 'wb') as f:
        return f.write(time)

def mod_time_check(fpath, time_previous):
    """compares file modified time to time_previous"""
    st=os.stat(fpath)    
    mtime=dt.datetime.fromtimestamp(st.st_mtime)
    if mtime>time_previous:
        return fpath
    else:
        return None

def file_copy(fpath, dir_dsts):
    """copy fpath to dir_dsts"""
    for dst in dir_dsts:
        shutil.copy2(fpath, dst)

def file_type_check(fpath, file_types):
    """check if file extension in file_types"""
    _, fileExtension = os.path.splitext(fpath)
    if fileExtension.lower() in file_types:
        return True
    else:
        return False
    
def dir_create(dir_path):
    """create a direcory if not already existing"""
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
   
def create_logger(save_file):
    """creates a logger with some default settings and writes output to save_file"""
    logger = logging.getLogger("spider")
    logger.setLevel(logging.DEBUG)
    h1 = logging.FileHandler(save_file)
    f1 = logging.Formatter("%(levelname)s %(asctime)s %(message)s")
    h1.setFormatter(f1)
    logger.addHandler(h1)
    return logger
    
def time_stamp(time_current, fmt='%Y-%m-%d-%H-%M-%S'):
    """strftime shortcut"""
    return time_current.strftime(fmt)


def list_from_file(fp):
    """fp is rows of directories seperated by carraige return"""
    with open(fp,"rb") as f:
        files = f.readlines()
        return [os.path.normcase(f.strip()) for f in files]


if __name__ == "__main__":
       
    FILE_TYPE = [".txt"] #<-keep file extensions lowercase here
    DIR_SEARCH = list_from_file("config/search_these_directories.txt")
    DIR_SKIP = list_from_file("config/skip_these_directories.txt")
    DIR_SKIP.append(os.getcwd()) #<-skip the directory where the code is running
    FILE_SKIP = list_from_file("config/skip_these_files.txt")
    DIR_ALL = "files_all"
    DIR_UPDATE = "files_update"
    LOG_LAST_RUN ="last_run_time/LAST_RUN.txt"
    FMT='%Y-%m-%d-%H-%M-%S'
    
    time_current = dt.datetime.now()
    time_current_string = time_current.strftime(FMT)
    time_previous = time_read(LOG_LAST_RUN, FMT)
    folder_update = os.path.join(DIR_UPDATE,time_current_string)
    logger = create_logger('logs/'+time_current_string+'.log')
    logger.info("Searching for these file extensions: {} modified after: {}".format(FILE_TYPE, time_previous))

    for dir_search in DIR_SEARCH:
        for root,dirs,files in os.walk(dir_search):
            print("hey Dan, I am here: ", root)
            logger.debug("Looking here: root: {}".format(root))
            if os.path.normcase(root) in DIR_SKIP:
                files[:] = []
                dirs[:] = []
                logger.info("DIR_SKIP found, skipping: root: {}, dirs: {}, files: {}".format(root,dirs,files))
            for bad_file_path in FILE_SKIP:
                bad_file_root, bad_file_name = os.path.split(bad_file_path)
                if bad_file_name in files and bad_file_root == os.path.normcase(root):
                    files.remove(bad_file_name)
                    logger.info("Skipping bad file from root: {} file: {}".format(root, bad_file_name))
            for fname in files:
                if not file_type_check(fname, FILE_TYPE):
                    continue
                fpath=os.path.join(root,fname)
                file_ans=mod_time_check(fpath, time_previous)
                if file_ans is not None:
                    dir_create(folder_update)
                    try:
                        file_copy(file_ans, [folder_update])
                        logger.info("Copied file: {}".format(file_ans))
                    except Exception, e:
                        logger.error("Tried but failed to to copy file: {}".format(file_ans), exc_info=True)
    else:
        time_write(LOG_LAST_RUN, time_current_string)
        logger.info("Run complete")
