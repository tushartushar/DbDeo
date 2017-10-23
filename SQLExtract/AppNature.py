# This program identifies for each repo in a given list
# if the enclosed application is mobile-, web-, or desktop-based.

import os
import csv
import re


def infer_app_nature(repoStoreRoot, repoResultRoot, plMetricsFile):
    logFile = os.path.join(repoResultRoot, 'logAppNature.txt')
    resultFile = os.path.join(repoResultRoot, 'appNature.csv')

    selectedRepos = []
    for dir in os.listdir(repoStoreRoot):
        if os.path.isdir(os.path.join(repoStoreRoot, dir)):
            selectedRepos.append(dir)

    repos = {}
    header = {}
    with open(plMetricsFile, 'r') as f:
        reader = csv.reader(f)
        firstLine = True
        for row in reader:
            if firstLine:      # separate header
                header[row[0]] = row[1:]
                firstLine = False
                continue
            if row[0] in selectedRepos:
                repos[row[0]] = [int(r) for r in row[1:]]

    indexPL = {}
    lang = {}
    i = 0
    for pl in header['repo']:
        indexPL[pl] = i
        lang[i] = pl
        i += 1

    log = ''
    result = ''
    i = 0
    for repo, metrics in repos.items():
        i += 1
        print(str(i) + ' ' + repo)
        log += repo + '\n'
        androidFile = False     # AndroidManifest.xml
        iosFile = False         # AppDelegate
        webStatic = False       # folder named static
        webCSS = False          # folder named css
        webPublic = False       # folder named public_html
        for root, dirs, files in os.walk(os.path.join(repoStoreRoot, repo)):
            files = [f for f in files if not f[0] == '.']
            dirs[:] = [d for d in dirs if not d[0] == '.']
            for d in dirs:
                if d == 'static':
                    webStatic = True
                    #log += '  static dir: ' + d + '\n'
                elif d == 'css':
                    webCSS = True
                    #log += '  css dir: ' + d + '\n'
                elif d == 'public_html':
                    webPublic = True
                    #log += '  public_html dir: ' + d + '\n'
            for f in files:
                if os.path.exists(os.path.join(root, f)):
                    if f == 'AndroidManifest.xml':
                        androidFile = True
                        log += '  Android file: ' + f + '\n'
                    elif re.match(r'AppDelegate(\.[mh])?$', f):
                        iosFile = True
                        log += '  ios file: ' + f + '\n'

        maxIndex = 0
        maxIndex2 = 0
        #print(metrics)
        # remove total files and lines
        orderedMetrics = sorted(metrics[1:-1], reverse = True)
        #print(orderedMetrics)
        for index, value in enumerate(metrics):
            if value == orderedMetrics[0]:
                maxIndex = index
            if value == orderedMetrics[1]:
                maxIndex2 = index

        mostUsedLang = lang[maxIndex]
        mostUsedLang2 = lang[maxIndex2]

        log += '  has Android file: ' + str(androidFile) + '\n'
        log += '  has ios file: ' + str(iosFile) + '\n'
        log += "  has dir 'static': " + str(webStatic) + '\n'
        log += "  has dir 'css': " + str(webCSS) + '\n'
        log += "  has dir 'public_html': " + str(webPublic) + '\n'
        log += '  most used language: ' + mostUsedLang + '\n'
        log += '  second most used language: ' + mostUsedLang2 + '\n'

        if androidFile and mostUsedLang == 'java':
            log += repo + ' is a mobile (Android) application\n'
            result += repo + ',mobile,Android\n'
        elif iosFile and mostUsedLang == 'objc':
            log += repo + ' is a mobile (ios) application\n'
            result += repo + ',mobile,ios\n'
        elif mostUsedLang == 'html' or (webStatic or webCSS or webPublic) and mostUsedLang in ['php', 'aspx', 'xml', 'py']:
            log += repo + ' is a web application\n'
            result += repo + ',web\n'
        else:
            log += repo + ' is a desktop application\n'
            result += repo + ',desktop\n'

        log += '\n'

        if i % 100 == 0:
            with open(logFile, 'a') as f:
                f.write(log)
                log = ''
            with open(resultFile, 'a') as f:
                f.write(result)
                result = ''

    if len(log) > 0:
        with open(logFile, 'a') as f:
            f.write(log)
    if len(result) > 0:
        with open(resultFile, 'a') as f:
            f.write(result)
    return resultFile

'''
print(indexPL)
print(lang)
print(selectedRepos[:10])
print(repos)
print(index)
print(repos['zikula_core'][index['java']])
print(repos['zikula_core'][index['php']])
'''
