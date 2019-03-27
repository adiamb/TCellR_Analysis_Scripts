
import glob
import copy
import re
from collections import OrderedDict
from collections import defaultdict

def ParseFile(FileString):
	calls = defaultdict(str)
	f_in=open(FileString, 'rb')
	for n, line in enumerate(f_in):
		if n>1:
			lin_parse= line.strip().split(',')
			print lin_parse
			makeBC = lin_parse[1]+'_'+lin_parse[2]
			calls[makeBC] += line.strip()+'$'
	f_in.close()
	return calls

def ParseRclUsage(RclList, chain):
	UsageMasterDict = defaultdict(lambda:defaultdict(str))
	FamsFound = set()
	for file in RclList:
		if file:
			with open(file) as infile:
				for line in infile:
					parse_line = line.strip().split(',')
					if chain == 'alpha':
						if parse_line[1] == 'a' and re.search(r'(TRAV|TRAJ)', parse_line[3]):
							if 'C1GJWACXX' in line:
								make_sample_key = '_'.join(parse_line[0].split('_')[:2])+'_'+parse_line[2]
							else:
								make_sample_key=parse_line[0].split('_')[0]+'_'+parse_line[2]
								make_family_key = parse_line[3]

					elif chain == 'beta':
						if parse_line[1] == 'b' and re.search(r'TRBV', parse_line[3]):
							if 'C1GJWACXX' in line:
								make_sample_key = '_'.join(parse_line[0].split('_')[:2])+'_'+parse_line[2]
							else:
								make_sample_key=parse_line[0].split('_')[0]+'_'+parse_line[2]
								make_family_key = parse_line[3]
					FamsFound.add(make_family_key)
					UsageMasterDict[make_sample_key][make_family_key] = parse_line[4]
	return[UsageMasterDict, FamsFound]


def WriteToFile(Headers, UsageDict, Outfile, calls):
	OutF=open(Outfile, 'wb')
	OutF.write('DBID,SEQ,BC,CELLTYPE,DBID2,CHAIN,'+','.join(Headers)+'\n')
	for k, v in UsageDict.items():
		if k in calls:
			GetSample = calls.get(k)
			OutF.write(GetSample)
			for fam in Headers:
				if fam in v:
					OutF.write(','+v.get(fam))
				else:
					OutF.write(','+'NA')
			OutF.write('\n')
	OutF.close()

FileString ='/media/labcomp/HDD2/RCL_FILES_AUG23_2017/DBIDS_ALPHA_WITH_BC_MARCH6_2018.txt'
calls = ParseFile(FileString)
RclList=glob.glob('/media/labcomp/HDD2/RCL_FILES_AUG23_2017/BASELINE_USAGE/*.rcl')
ParsedUsages=ParseRclUsage(RclList=RclList, chain='alpha')
UsageHeaders = [i for i in ParsedUsages[1]]
UsageMaster = ParsedUsages[0]

WriteToFile(Headers=UsageHeaders,
	UsageDict=UsageMaster,
	Outfile='/media/labcomp/HDD2/RCL_FILES_AUG23_2017/BASELINE_USAGE/MAIN_TRA_USAGE_MARCH26_2019.csv',
	calls=calls)						


# outfile= open('MAIN_TRA_USAGE_MARCH26_2019.out', 'w')
# outfile.write('DBID,SEQ,BC,cell_type,dbid2,chain,'+','.join(UsageHeaders)+'\n')
# for key, value in main_usage_dic.iteritems():
# 	if key in ALPHA_calls:
# 		get_sample = ALPHA_calls.get(key)
# 		outfile.write(get_sample+',')
# 		for key2, value2 in value.iteritems():
# 			outfile.write(value2+',')
# 		outfile.write('\n')
# outfile.close() 