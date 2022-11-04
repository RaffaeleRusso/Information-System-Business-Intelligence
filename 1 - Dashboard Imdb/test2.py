str1="ciao,eefe,sfef"
str1=str1.replace(",","")

print(str1)







def dopo():
        if unico==True:
        for s in states:
            tmp=df["Genre"].str.contains(s, case=False)
            if s==list(states)[0]:
                fine=tmp
            fine=fine & tmp
    return fine
    else:



    fine=[]
    tmp=[]
    for i,k in df.iterrows():
        k["Genre"]=k["Genre"].split(",")
        enable=True
        for i in k["Genre"]:
            if i not in states:
                enable=False
        fine.append(enable)
    fine = pd.DataFrame (fine, columns = ['Condition'])
    print(fine)



    fine=[]
    tmp=[]
    for i,k in df.iterrows():
        k["Genre"]=k["Genre"].split(",")
        enable=True
        for i in k["Genre"]:
            if i not in states:
                enable=False
        fine.append(enable)
    return fine