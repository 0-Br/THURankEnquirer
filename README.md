# THURankEnquirer

清华大学学生成绩排名批量查询与统计工具。

通过问卷星成绩查询接口，批量获取学生的年级/班级排名百分位数据，并按自定义评分规则汇总输出。

## 工作流程

本项目包含三个脚本，按顺序执行：

### 1. `extraction.py` — 数据预处理

从原始花名册 Excel 中提取学号、姓名和身份证号，筛选指定年级的学生，输出为 CSV。

### 2. `crawler.py` — 排名数据爬取

逐条读取 CSV 中的身份证号，向问卷星查询接口发送 POST 请求，解析返回页面中的排名信息。支持失败重试与随机延时。爬取结果以 pickle 格式保存。

### 3. `results.py` — 评分与分档

加载爬取结果，根据四项排名百分位（年级全部、年级必限、班级全部、班级必限）计算综合得分，按分数段（A–F）分 sheet 导出至 Excel。

## 依赖

- Python 3
- pandas
- requests
- beautifulsoup4
- fake-useragent
- tqdm
- openpyxl

## 注意

`data/` 目录包含个人敏感信息，已通过 `.gitignore` 排除，不会提交至仓库。
