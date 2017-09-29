import os

METRIC_FILE_PATH = "/home/tushar/repos/results/metrics.csv"
APPNATURE_FILE_PATH = "/home/tushar/repos/results/appNature.csv"
ORM_FILE_PATH = "/home/tushar/repos/results/orm.csv"
PRGLANG_FILE_PATH = "/home/tushar/repos/results/progLang.csv"
AGGREGATED_FILE_PATH = "/home/tushar/repos/results/dbSmellData/aggregated_results.csv"

METRIC_NEW_FILE_PATH = "/home/tushar/repos/results/metrics_sanitized.csv"
APPNATURE_NEW_FILE_PATH = "/home/tushar/repos/results/appNature_sanitized.csv"
ORM_NEW_FILE_PATH = "/home/tushar/repos/results/orm_sanitized.csv"
PRGLANG_NEW_FILE_PATH = "/home/tushar/repos/results/progLang_sanitized.csv"
AGGREGATED_NEW_FILE_PATH = "/home/tushar/repos/results/dbSmellData/aggregated_results_sanitized.csv"

def write_line(fileName, text):
   try:
     with open(fileName, "a", errors='ignore') as f:
        f.write(text + "\n")
   except:
     print("Exepction while writing file.")
     pass


def sanitize_metrics_file(prj_dict):
    proj_counter = 1
    is_first_line = True
    with open(METRIC_FILE_PATH, "r", errors='ignore') as r:
        for line in r:
            line = line.strip()
            if is_first_line:
                write_line(METRIC_NEW_FILE_PATH, line)
                is_first_line = False
                continue
            if line == "":
                continue
            repo, select, create, insert, update, index, *rest = line.split(",")
            if repo.startswith('training') | repo.startswith('opensource') | repo.startswith('successfully') | repo.startswith('results'):
                continue
            total_sql = int(select) + int(create) + int(insert) + int(update) + int(index)
            if total_sql > 0:
                repo = repo.strip(".sql")
                new_prj_name = "P" + str(proj_counter)
                proj_counter = proj_counter+1
                prj_dict[repo] = new_prj_name
                write_line(METRIC_NEW_FILE_PATH, new_prj_name + "," + str(select) + "," + str(create) + "," + str(insert) + "," + str(update) + "," + str(index))

def sanitize_appnature_file(prj_dict):
    with open(APPNATURE_FILE_PATH, "r", errors='ignore') as r:
        for line in r:
            line = line.strip()
            if line == "":
                continue
            repo, appnature, *rest = line.split(",")
            if repo in prj_dict:
                write_line(APPNATURE_NEW_FILE_PATH, prj_dict[repo] + "," + appnature)

def sanitize_orm_file(prj_dict):
    with open(ORM_FILE_PATH, "r", errors='ignore') as r:
        for line in r:
            line = line.strip()
            if line == "":
                continue
            repo, orm, *rest = line.split(",")
            if repo in prj_dict:
                write_line(ORM_NEW_FILE_PATH, prj_dict[repo] + "," + orm)

def sanitize_progLang_file(prj_dict):
    is_first_line = True
    with open(PRGLANG_FILE_PATH, "r", errors='ignore') as r:
        for line in r:
            line = line.strip()
            if is_first_line:
                write_line(PRGLANG_NEW_FILE_PATH, line)
                is_first_line = False
                continue
            if line == "":
                continue
            strs = line.split(",")
            if strs[0] in prj_dict:
                new_line = prj_dict[strs[0]]
                for i in range(1, 17):
                    new_line = new_line + "," + str(strs[i])
                write_line(PRGLANG_NEW_FILE_PATH, new_line)


def sanitize_aggregated_file(prj_dict):
    is_first_line = True
    with open(AGGREGATED_FILE_PATH, "r", errors='ignore') as r:
        for line in r:
            line = line.strip()
            if is_first_line:
                write_line(AGGREGATED_NEW_FILE_PATH, line)
                is_first_line = False
                continue
            if line == "":
                continue
            strs = line.split(",")
            if strs[0] in prj_dict:
                new_line = prj_dict[strs[0]]
                for i in range(1, 14):
                    new_line = new_line + "," + str(strs[i])
                write_line(AGGREGATED_NEW_FILE_PATH, new_line)

def remove_old_files():
    if(os.path.exists(METRIC_NEW_FILE_PATH)):
        os.remove(METRIC_NEW_FILE_PATH)
    if(os.path.exists(APPNATURE_NEW_FILE_PATH)):
        os.remove(APPNATURE_NEW_FILE_PATH)
    if(os.path.exists(ORM_NEW_FILE_PATH)):
        os.remove(ORM_NEW_FILE_PATH)
    if(os.path.exists(PRGLANG_NEW_FILE_PATH)):
        os.remove(PRGLANG_NEW_FILE_PATH)
    if(os.path.exists(AGGREGATED_NEW_FILE_PATH)):
        os.remove(AGGREGATED_NEW_FILE_PATH)


prj_dict = {}
remove_old_files()
sanitize_metrics_file(prj_dict)
sanitize_appnature_file(prj_dict)
sanitize_orm_file(prj_dict)
sanitize_progLang_file(prj_dict)
sanitize_aggregated_file(prj_dict)