#!/usr/bin/env python

from app import chinese_phrase_graph

chinese_phrase_graph.add_phrase("口", meaning="mouth")
chinese_phrase_graph.add_phrase("吃饭", meaning="to eat food")
chinese_phrase_graph.add_phrase("喝", meaning="to drink")
chinese_phrase_graph.add_phrase("咬", meaning="to bite")
chinese_phrase_graph.add_phrase("喵", meaning="to meow, like a cat")
chinese_phrase_graph.add_phrase("猫", meaning="cat")
chinese_phrase_graph.add_phrase("狗", meaning="dog")
chinese_phrase_graph.add_phrase("渴", meaning="thirsty")
chinese_phrase_graph.add_phrase("你好", meaning="hello")
chinese_phrase_graph.add_phrase("您好", meaning="hello, but polite you")
chinese_phrase_graph.add_phrase("高兴", meaning="happy")
chinese_phrase_graph.add_phrase("早", meaning="sunrise")
chinese_phrase_graph.add_phrase("旦", meaning="early morning")
chinese_phrase_graph.add_phrase("日", meaning="sun")
chinese_phrase_graph.add_phrase("日本", meaning="Japan")
chinese_phrase_graph.add_phrase("好久不见", meaning="long time no see")
chinese_phrase_graph.add_phrase("再见", meaning="goodbye")
chinese_phrase_graph.add_phrase("见", meaning="to see")
chinese_phrase_graph.add_phrase("你怎么样", meaning="how are you doing?")
chinese_phrase_graph.add_phrase("什么", meaning="what?")
chinese_phrase_graph.add_phrase("最近", meaning="recently")
chinese_phrase_graph.add_phrase("呷", meaning="to sip")
chinese_phrase_graph.add_phrase("多少", meaning="how many?")
chinese_phrase_graph.add_phrase("名字", meaning="name")
chinese_phrase_graph.add_phrase("说", meaning="to speak")

chinese_phrase_graph.add_phrase("女朋友", meaning="girlfriend")
chinese_phrase_graph.add_phrase("朋友", meaning="friend")
chinese_phrase_graph.connect_phrases("女朋友", "朋友")

chinese_phrase_graph.add_phrase("书", meaning="book")
chinese_phrase_graph.add_phrase("看", meaning="to read")
chinese_phrase_graph.connect_phrases("书", "看")

chinese_phrase_graph.add_phrase("电话", meaning="telephone ☎️")
chinese_phrase_graph.add_phrase("号码", meaning="numbers")
chinese_phrase_graph.add_phrase("电话号码", meaning="telephone number")

chinese_phrase_graph.add_phrase("电脑", meaning="computer")
chinese_phrase_graph.connect_phrases("电", "电脑")

chinese_phrase_graph.add_phrase("最", meaning="most")
chinese_phrase_graph.add_phrase("最爱", meaning="favourite")
chinese_phrase_graph.connect_phrases("最", "最爱")

chinese_phrase_graph.add_phrase("每天", meaning="every day")

chinese_phrase_graph.add_phrase("下午", meaning="afternoon")

chinese_phrase_graph.add_phrase("喜欢", meaning="to like")

chinese_phrase_graph.add_phrase("玩", meaning="to play")
chinese_phrase_graph.add_phrase("游戏", meaning="game")
chinese_phrase_graph.connect_phrases("玩", "游戏")

chinese_phrase_graph.add_phrase("孩子", meaning="children")

chinese_phrase_graph.add_phrase("老师", meaning="teacher")
chinese_phrase_graph.add_phrase("学生", meaning="student")
chinese_phrase_graph.connect_phrases("老师", "学生")

chinese_phrase_graph.add_phrase("漂亮", meaning="pretty")

chinese_phrase_graph.connect_phrases("口", "吃饭", note="Look at the 口 radical")
chinese_phrase_graph.connect_phrases("口", "喝")
chinese_phrase_graph.connect_phrases("口", "呷")
chinese_phrase_graph.connect_phrases("呷", "喝")
chinese_phrase_graph.connect_phrases("口", "咬")
chinese_phrase_graph.connect_phrases("口", "喵")
chinese_phrase_graph.connect_phrases("猫", "喵")
chinese_phrase_graph.connect_phrases("猫", "狗", note="Notice the matching radical!")
chinese_phrase_graph.connect_phrases("喝", "渴")
chinese_phrase_graph.connect_phrases("你好", "您好")
chinese_phrase_graph.connect_phrases("早", "旦")
chinese_phrase_graph.connect_phrases("早", "日")
chinese_phrase_graph.connect_phrases("日", "旦")
chinese_phrase_graph.connect_phrases("日", "日本")
chinese_phrase_graph.connect_phrases("再见", "见")
chinese_phrase_graph.connect_phrases("好久不见", "见")
chinese_phrase_graph.connect_phrases("你怎么样", "什么")
chinese_phrase_graph.connect_phrases(
    "多少", "号码", note="Use 号码 when asking how many of something"
)
chinese_phrase_graph.connect_phrases("电话号码", "电话")
chinese_phrase_graph.connect_phrases("电话号码", "号码")

chinese_phrase_graph.add_phrase("车子", meaning="car/vehicle 🚗")
chinese_phrase_graph.add_phrase(
    "火车", meaning="train 🚄", notes="a fire-powered vehicle is a train"
)
chinese_phrase_graph.connect_phrases("车子", "火车")

chinese_phrase_graph.add_phrase(
    "公车", meaning="bus 🚌", notes="a public vehicle is a bus"
)
chinese_phrase_graph.connect_phrases("车子", "公车")
chinese_phrase_graph.add_phrase("公", meaning="public")
chinese_phrase_graph.connect_phrases("公", "公车")

chinese_phrase_graph.add_phrase("马车", meaning="a horse-drawn cart")
chinese_phrase_graph.connect_phrases("车子", "马车")

chinese_phrase_graph.add_phrase(
    "电车",
    meaning="a tram",
    notes="an electric vehicle is a tram (rather than an electric car, because trams predate electric cars)",
)
chinese_phrase_graph.connect_phrases("车子", "电车")

chinese_phrase_graph.add_phrase("电动汽车", meaning="an electric car ⚡🚗")
chinese_phrase_graph.connect_phrases("车子", "电动汽车")
chinese_phrase_graph.connect_phrases("电车", "电动汽车")

chinese_phrase_graph.add_phrase("几", meaning="how many?")
chinese_phrase_graph.connect_phrases("几", "多少")

chinese_phrase_graph.add_phrase("电视", meaning="television 📺")

chinese_phrase_graph.add_phrase("电", meaning="electricity ⚡")
chinese_phrase_graph.connect_phrases("电", "电话")
chinese_phrase_graph.connect_phrases("电", "电动汽车")
chinese_phrase_graph.connect_phrases("电", "电视")

chinese_phrase_graph.connect_phrases("电", "电车")
