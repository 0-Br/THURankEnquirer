import pandas as pd


if __name__ == '__main__':
    df = pd.read_excel('data\\weiyang.xlsx', header=0)
    df = df[['身份证-序号', '学号', '姓名']]
    df['身份证号'] = df['身份证-序号'].apply(lambda id: id[:18])
    df = df.drop('身份证-序号', axis=1).drop_duplicates()
    df = df[df['学号'].between(2021000000, 2022000000)].reset_index(drop=True)

    df.to_csv('data\\namelist.csv', index=None)
