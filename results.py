import pandas as pd
import pickle

def judge(case:str) -> int:
    score = 0
    case = str(case)
    if case == "前30%":
        score += 25
    if case == "30%-50%":
        score += 15
    if case == "50%-80%":
        score += 10
    if case == "80%-100%":
        score += 5
    return score

def check(row):
    return judge(row["年级排名(全部)"]) + judge(row["年级排名(必限)"]) + judge(row["班级排名(全部)"]) + judge(row["班级排名(必限)"])


if __name__ == '__main__':
    with open("data\\results.pkl", 'rb') as f:
        info = pickle.load(f)
    df = pd.concat([pd.Series(value) for value in info.values()], axis=1).stack().unstack(0)
    df['综合得分'] = df.apply(check, axis=1)

    with pd.ExcelWriter("data\\results.xlsx") as writer:
        df.to_excel(writer, sheet_name="All")
        df[df['综合得分'] >= 90].to_excel(writer, sheet_name="A")
        df[(df['综合得分'] >= 75) & (df['综合得分'] < 90)].to_excel(writer, sheet_name="B")
        df[(df['综合得分'] >= 60) & (df['综合得分'] < 75)].to_excel(writer, sheet_name="C")
        df[(df['综合得分'] >= 45) & (df['综合得分'] < 60)].to_excel(writer, sheet_name="D")
        df[(df['综合得分'] >= 30) & (df['综合得分'] < 45)].to_excel(writer, sheet_name="E")
        df[df['综合得分'] < 30].to_excel(writer, sheet_name="F")
