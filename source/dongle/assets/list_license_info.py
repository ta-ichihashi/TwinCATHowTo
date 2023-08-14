import xml.etree.ElementTree as ET
import os
import csv

current_dir = os.getcwd()

report = list()
report.append(['File','LicenseID', 'SystemID', 'PerformanceLevel', 'Licenses'])

for fname in os.listdir():
    fname = fname.upper()
    if ("TCLRQ" in fname) or ("TCLRS" in fname):
        # XMLファイルを解析
        tree = ET.parse(current_dir + '/' + fname)

        # XMLを取得
        root = tree.getroot()
        #root['TcLicenseInfo']

        line = list()

        line.append(fname)
        line.append(root.find('LicenseInfo').find('PurchaseOrder').text)
        line.append(root.find('LicenseInfo').find('SystemId').text[1:-1])
        line.append(root.find('LicenseInfo').find('SystemId').get('Level'))

        licenses = list()
        for license in root.find('LicenseInfo').iter('License'):
            licenses.append(f"{license.find('Name').text}({license.find('OrderNo').text})")
        line.append(','.join(licenses))
        report.append(line)



with open('report.csv', 'w', newline='') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
    writer.writerows(report)