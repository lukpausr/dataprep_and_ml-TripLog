import pandas as pd 

datas = [1, 2 , 3]
datas2 = [4,5,6]
columnsname = ["a", "b", "c"]

dataFrame1 = pd.DataFrame(data = [datas], columns = columnsname, index= None)
dataFrame2 = pd.DataFrame(data = [datas2], columns = columnsname, index = None)
dataFrame = pd.concat([dataFrame1, dataFrame2])
print(dataFrame)


#s1 = pd.Series([1,2,3])
#s2 = pd.Series(['a','b','c'])

#df = pd.DataFrame([list(s1), list(s2)],  columns =  ["C1", "C2", "C3"])
#print df