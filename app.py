# 导入需要的工具，不用管，复制就行
import streamlit as st
import math
import pandas as pd

# ---------------------- 1. 核心配置：4个维度（不用改）----------------------
DIMENSIONS = [
    "社交能量",  # -2低能耗 ←→ +2高能耗
    "主动程度",  # -2被动 ←→ +2主动
    "内容重点",  # -2学术深聊 ←→ +2社交/资源
    "节奏偏好"   # -2会后深耕 ←→ +2当场推进
]

# ---------------------- 2. 20+会议社交人格（你可以随便加/改）----------------------
ROLES = [
    {
        "name": "社交节能保",
        "coords": [-2, -1, -1, -2],
        "tagline": "低能耗社交选手，只聊有价值的内容",
        "strengths": ["完全不内耗", "倾听能力拉满", "深度交流精准"],
        "weaknesses": ["容易错过拓展机会", "很少主动开启话题"],
        "openers": [
            "您好，请问您这次会议最关注哪个方向的研究？",
            "我之前读过您的XX论文，对里面的XX方法特别感兴趣，想请教一下"
        ],
        "followup": "今天和您交流收获特别大，后续我把相关的文献整理好发您邮箱，保持联系~",
        "best_match": "海报区守卫者",
        "conflict_match": "会后饭局社达者"
    },
    {
        "name": "海报区守卫者",
        "coords": [-1, 0, -2, -1],
        "tagline": "深耕海报内容，学术细节控",
        "strengths": ["对研究细节理解极深", "不怕被提问", "学术交流精准"],
        "weaknesses": ["很少离开海报区", "社交范围窄"],
        "openers": [
            "您好，我对您海报里的XX实验特别感兴趣，想请教一下实验设计",
            "请问您这个研究的后续有什么新的进展吗？"
        ],
        "followup": "感谢您的解答，我后续把我的相关实验数据整理好，和您再交流~",
        "best_match": "壁报走访记录员",
        "conflict_match": "展台薅羊毛者"
    },
    {
        "name": "闪现提问侠",
        "coords": [1, 2, -1, 2],
        "tagline": "分会场提问天花板，当场就把问题聊透",
        "strengths": ["逻辑清晰", "敢提问", "当场就能建立联系"],
        "weaknesses": ["容易给社恐同学压力", "提问太密集"],
        "openers": [
            "老师您好，刚才您的报告里XX观点我特别认同，想补充请教一个问题",
            "您好，我是XX大学的博士生，刚才您的报告给我特别大的启发"
        ],
        "followup": "刚才您的解答解决了我困扰很久的问题，后续有新的想法再和您请教~",
        "best_match": "主题串讲者",
        "conflict_match": "社交节能保"
    },
    {
        "name": "资源对接官",
        "coords": [2, 2, 2, 1],
        "tagline": "会议人脉天花板，合作机会挖掘机",
        "strengths": ["人脉拓展能力强", "资源整合快", "情商拉满"],
        "weaknesses": ["学术深聊容易浅尝辄止", "社交太分散"],
        "openers": [
            "您好，我是XX大学的博士生，我们团队最近在做XX方向，感觉和您的研究特别契合，想看看有没有合作的机会",
            "您好，久仰您的大名，终于有机会当面和您交流"
        ],
        "followup": "今天和您聊的合作方向我特别看好，后续我把我们团队的相关资料发您，我们再细聊~",
        "best_match": "企业展位桥梁人",
        "conflict_match": "分会场潜伏者"
    },
    {
        "name": "伊丽莎白点头机",
        "coords": [-1, -2, 0, 0],
        "tagline": "倾听型社交选手，全场最捧场的人",
        "strengths": ["完全不冷场", "给足对方情绪价值", "零社交压力"],
        "weaknesses": ["很少主动表达自己的观点", "容易被带着走"],
        "openers": [
            "您说的这个点我太有共鸣了",
            "哇，这个研究也太有意思了，您能再多讲讲吗？"
        ],
        "followup": "今天听您讲了这么多，我真的学到特别多，感谢您的分享~",
        "best_match": "主题串讲者",
        "conflict_match": "闪现提问侠"
    },
    {
        "name": "会后饭局社达者",
        "coords": [2, 1, 2, 2],
        "tagline": "饭局社交天花板，线下关系破冰王者",
        "strengths": ["氛围组组长", "快速拉近关系", "线下社交能力拉满"],
        "weaknesses": ["学术交流不够深入", "容易喝多耽误事"],
        "openers": [
            "晚上主办方的晚宴您去吗？咱们可以坐一桌多聊聊",
            "我知道附近有一家特别好吃的店，晚上一起去吃个便饭，边吃边聊？"
        ],
        "followup": "今天晚上聊得太开心了，后续常联系，有机会再一起吃饭~",
        "best_match": "合影发起人",
        "conflict_match": "社交节能保"
    },
    {
        "name": "分会场潜伏者",
        "coords": [-2, -2, -1, -1],
        "tagline": "沉浸式听报告，零社交压力选手",
        "strengths": ["吸收信息效率极高", "完全不内耗", "专注度拉满"],
        "weaknesses": ["几乎不拓展人脉", "错过很多交流机会"],
        "openers": [
            "您好，刚才听了您的报告，有一个小问题想请教您",
            "您好，您的报告特别有启发，感谢分享"
        ],
        "followup": "感谢您的解答，后续我再仔细研读您的论文，有问题再向您请教~",
        "best_match": "研讨会打卡王",
        "conflict_match": "资源对接官"
    },
    {
        "name": "壁报走访记录员",
        "coords": [0, 0, -2, -2],
        "tagline": "海报区深度调研者，学术信息挖掘机",
        "strengths": ["信息收集能力极强", "研究视野广", "细节记得超牢"],
        "weaknesses": ["交流多停留在学术层面", "很少拓展私人联系"],
        "openers": [
            "您好，我正在做XX方向的研究，看到您的海报特别相关，想记录一下您的研究细节",
            "请问您这个研究的数据集是公开的吗？我后续想复现一下"
        ],
        "followup": "感谢您的分享，对我的研究帮助特别大，后续有进展再和您交流~",
        "best_match": "海报区守卫者",
        "conflict_match": "展台薅羊毛者"
    },
    {
        "name": "展台薅羊毛者",
        "coords": [1, 0, 2, 0],
        "tagline": "企业展位福利收割机，会议周边收集达人",
        "strengths": ["信息灵通", "不怕和企业方交流", "薅羊毛从不手软"],
        "weaknesses": ["学术交流占比少", "容易在展位耽误太多时间"],
        "openers": [
            "您好，请问你们这个产品对高校学生有免费的使用权限吗？",
            "您好，想了解一下你们这个数据库的高校订阅方案"
        ],
        "followup": "感谢您的介绍，后续我和导师沟通一下，有需求再和您联系~",
        "best_match": "企业展位桥梁人",
        "conflict_match": "壁报走访记录员"
    },
    {
        "name": "会后笔记博主",
        "coords": [-1, -1, -1, -2],
        "tagline": "会议内容全记录，会后复盘王者",
        "strengths": ["信息整理能力极强", "复盘逻辑清晰", "会后跟进超稳"],
        "weaknesses": ["当场交流不够主动", "容易沉浸在记笔记里错过互动"],
        "openers": [
            "您好，刚才您的报告我记了很多笔记，有几个点想再和您确认一下",
            "您好，您的报告内容特别干货，想请教一下XX部分的细节"
        ],
        "followup": "您好，我是今天会议上和您交流的XX，这是我整理的会议笔记，和您分享一下，后续保持联系~",
        "best_match": "时间管理指挥",
        "conflict_match": "闪现提问侠"
    }
]

# ---------------------- 3. 12道测试题（你可以随便加/改）----------------------
QUESTIONS = [
    {
        "title": "会议开场的前10分钟，你会做什么？",
        "options": [
            {
                "text": "主动和周围的人打招呼、自我介绍，快速认识新朋友",
                "weights": [2, 2, 1, 1]
            },
            {
                "text": "先逛一圈海报区，看看感兴趣的研究，遇到同方向的人再搭话",
                "weights": [0, 0, -2, -1]
            },
            {
                "text": "直接进分会场找个角落坐下，预习今天的报告内容，不主动社交",
                "weights": [-2, -2, -1, -1]
            },
            {
                "text": "先去企业展位逛一圈，看看有没有福利和合作资源",
                "weights": [1, 1, 2, 0]
            }
        ]
    },
    {
        "title": "分会场报告的问答环节，你会？",
        "options": [
            {
                "text": "有想问的问题立刻举手，当场就把疑问聊透",
                "weights": [1, 2, -1, 2]
            },
            {
                "text": "先把问题记下来，等报告结束后私下找讲者交流",
                "weights": [-1, -1, -1, -2]
            },
            {
                "text": "听别人提问就好，自己不主动举手",
                "weights": [-2, -2, 0, 0]
            },
            {
                "text": "借提问的机会介绍自己的研究，和讲者建立联系",
                "weights": [2, 2, 2, 1]
            }
        ]
    },
    {
        "title": "咖啡排队的时候，刚好遇到你领域里的大牛，你会？",
        "options": [
            {
                "text": "立刻上前自我介绍，说明自己对他的研究的关注",
                "weights": [2, 2, 1, 1]
            },
            {
                "text": "等对方点完单、空闲的时候，轻轻搭话请教一个学术问题",
                "weights": [0, 0, -2, -1]
            },
            {
                "text": "假装没看见，避免尴尬，等后续邮件联系",
                "weights": [-2, -2, 0, -2]
            },
            {
                "text": "主动帮对方付咖啡钱，顺势开启话题",
                "weights": [2, 2, 2, 2]
            }
        ]
    },
    {
        "title": "在海报区看到一张和你研究高度相关的海报，你会怎么开启对话？",
        "options": [
            {
                "text": "直接指出海报里的一个细节，请教实验设计和研究思路",
                "weights": [-1, 0, -2, -1]
            },
            {
                "text": "先夸海报做得好，再自我介绍，开启话题",
                "weights": [1, 1, 0, 0]
            },
            {
                "text": "先拍张照，等会后发邮件交流，不当场搭话",
                "weights": [-2, -2, -1, -2]
            },
            {
                "text": "聊完研究后，顺势加个微信/LinkedIn，后续保持联系",
                "weights": [1, 1, 2, 1]
            }
        ]
    },
    {
        "title": "连续社交2小时后，你感觉精力耗尽，你会？",
        "options": [
            {
                "text": "找个没人的角落歇10分钟，充好电再继续社交",
                "weights": [-2, -1, 0, -1]
            },
            {
                "text": "硬撑着继续和人交流，来都来了不能浪费机会",
                "weights": [2, 1, 2, 1]
            },
            {
                "text": "停止社交，专心听报告、记笔记，不勉强自己",
                "weights": [-2, -2, -1, 0]
            },
            {
                "text": "拉着刚认识的朋友去买咖啡，边喝边轻松聊，换个节奏充电",
                "weights": [0, 0, 2, 0]
            }
        ]
    },
    {
        "title": "会议晚宴/饭局，你会？",
        "options": [
            {
                "text": "主动坐到大牛/同行多的桌，全程主动开启话题",
                "weights": [2, 2, 2, 2]
            },
            {
                "text": "找认识的同学/同门坐一桌，不主动去别的桌社交",
                "weights": [-1, -1, 0, -1]
            },
            {
                "text": "不去饭局，回酒店整理今天的笔记和资料",
                "weights": [-2, -2, -1, -2]
            },
            {
                "text": "每桌都敬一杯酒，混个脸熟，认识更多人",
                "weights": [2, 2, 2, 1]
            }
        ]
    },
    {
        "title": "有人主动和你搭话，聊的内容你完全不感兴趣，你会？",
        "options": [
            {
                "text": "礼貌点头倾听，找机会结束对话，去聊自己感兴趣的内容",
                "weights": [-1, -1, 0, 0]
            },
            {
                "text": "顺着对方的话题聊，顺便拓展一下新的信息",
                "weights": [1, 0, 2, 0]
            },
            {
                "text": "全程微笑点头，不主动延伸话题，等对方自己结束",
                "weights": [-2, -2, 0, 0]
            },
            {
                "text": "直接说自己对这个话题不了解，换个双方都感兴趣的话题",
                "weights": [0, 1, 0, 0]
            }
        ]
    },
    {
        "title": "会议结束后，你会怎么跟进今天认识的人？",
        "options": [
            {
                "text": "当天晚上就发邮件/LinkedIn消息，附上交流的细节，保持联系",
                "weights": [1, 1, 1, 2]
            },
            {
                "text": "先整理好自己的笔记和资料，3天内再统一跟进",
                "weights": [-1, -1, -1, -1]
            },
            {
                "text": "加了联系方式就好，有需要的时候再联系，不刻意跟进",
                "weights": [-2, -2, 1, -2]
            },
            {
                "text": "拉个小群，把同方向的人都聚在一起，后续一起交流",
                "weights": [2, 2, 2, 1]
            }
        ]
    },
    {
        "title": "会议的平行分会场，你会怎么安排行程？",
        "options": [
            {
                "text": "提前做好时间表，每个分会场都去逛一圈，认识更多人",
                "weights": [2, 0, 2, 0]
            },
            {
                "text": "只去和自己研究高度相关的分会场，深耕内容",
                "weights": [-2, -1, -2, -1]
            },
            {
                "text": "不提前规划，走到哪个分会场感兴趣就进去听",
                "weights": [0, 0, 0, 0]
            },
            {
                "text": "每个分会场只听重点报告，剩下的时间用来社交和逛海报",
                "weights": [1, 0, 1, 0]
            }
        ]
    },
    {
        "title": "遇到和你研究方向完全相反的学者，你会？",
        "options": [
            {
                "text": "主动上前交流，辩论不同的研究思路，当场聊透",
                "weights": [2, 2, -1, 2]
            },
            {
                "text": "先听对方的观点，记下来，会后再找相关论文研读",
                "weights": [-2, -2, -1, -2]
            },
            {
                "text": "礼貌交流，不深入辩论，避免尴尬",
                "weights": [-1, -1, 0, 0]
            },
            {
                "text": "顺势加个联系方式，后续邮件里再深入交流学术观点",
                "weights": [0, 0, -1, -1]
            }
        ]
    },
    {
        "title": "会议上认识了同方向的博士生，你会？",
        "options": [
            {
                "text": "深度交流研究细节，互相分享实验经验和踩坑心得",
                "weights": [-1, 0, -2, -1]
            },
            {
                "text": "加个好友，后续一起吐槽读博日常，搭伴参加后续的会议",
                "weights": [1, 1, 2, 0]
            },
            {
                "text": "礼貌交流，分开后就不联系了",
                "weights": [-2, -2, 0, 0]
            },
            {
                "text": "看看有没有合作发论文的机会，深度绑定",
                "weights": [1, 1, 2, 1]
            }
        ]
    },
    {
        "title": "你的导师让你在会议上多认识领域里的大牛，你会？",
        "options": [
            {
                "text": "提前列好目标名单，会议上挨个找机会认识、交流",
                "weights": [2, 2, 1, 1]
            },
            {
                "text": "遇到了就主动打招呼，不刻意去找",
                "weights": [0, 0, 0, 0]
            },
            {
                "text": "只在报告的问答环节提问，让大牛对你有印象，不私下搭话",
                "weights": [-1, -1, -1, 0]
            },
            {
                "text": "让导师帮忙引荐，自己不主动上前",
                "weights": [-2, -2, 0, -1]
            }
        ]
    }
]

# ---------------------- 4. 核心算分函数（不用改）----------------------
def calculate_distance(user_coords, role_coords):
    """计算用户坐标和角色坐标的欧几里得距离，距离越小越匹配"""
    return math.sqrt(sum((u - r) ** 2 for u, r in zip(user_coords, role_coords)))

def normalize_score(total_score, question_count):
    """把分数归一化到 [-2, +2] 区间"""
    max_possible = question_count * 2
    min_possible = question_count * -2
    normalized = 2 * (total_score - min_possible) / (max_possible - min_possible) - 2
    return round(normalized, 2)

# ---------------------- 5. 网页界面搭建（不用改，想美化可以随便调）----------------------
# 网页基础配置
st.set_page_config(
    page_title="学术会议社交人格测试",
    page_icon="🎓",
    layout="centered"
)

# 网页标题
st.title("🎓 学术会议社交人格测试")
st.subheader("3分钟测出你的会议社交专属人设，解锁专属社交话术")
st.divider()

# 初始化session_state，存用户的答案和分数
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "user_scores" not in st.session_state:
    st.session_state.user_scores = [0, 0, 0, 0]
if "test_finished" not in st.session_state:
    st.session_state.test_finished = False

# 测试流程
if not st.session_state.test_finished:
    # 显示当前题目
    current_q = QUESTIONS[st.session_state.current_question]
    st.subheader(f"第 {st.session_state.current_question + 1}/{len(QUESTIONS)} 题")
    st.write(current_q["title"])

    # 显示选项
    user_choice = st.radio(
        "请选择最符合你的选项",
        options=range(len(current_q["options"])),
        format_func=lambda x: current_q["options"][x]["text"],
        key=f"q_{st.session_state.current_question}"
    )

    # 上一题/下一题按钮
    col1, col2 = st.columns(2)
    with col2:
        if st.button("下一题", use_container_width=True):
            # 累加分数
            selected_weights = current_q["options"][user_choice]["weights"]
            for i in range(4):
                st.session_state.user_scores[i] += selected_weights[i]
            
            # 进入下一题
            st.session_state.current_question += 1
            
            # 所有题答完，标记完成
            if st.session_state.current_question >= len(QUESTIONS):
                st.session_state.test_finished = True
                st.rerun()

else:
    # 测试完成，计算结果
    st.balloons()
    st.title("🎉 你的测试结果出来啦！")

    # 1. 归一化用户分数
    question_count = len(QUESTIONS)
    user_normalized = [
        normalize_score(st.session_state.user_scores[0], question_count),
        normalize_score(st.session_state.user_scores[1], question_count),
        normalize_score(st.session_state.user_scores[2], question_count),
        normalize_score(st.session_state.user_scores[3], question_count)
    ]

    # 2. 计算和所有角色的匹配度
    role_distances = []
    for role in ROLES:
        dist = calculate_distance(user_normalized, role["coords"])
        role_distances.append((role, dist))
    
    # 按距离排序，取最匹配的
    role_distances.sort(key=lambda x: x[1])
    main_role = role_distances[0][0]
    second_role = role_distances[1][0]

    # 3. 显示结果
    st.header(f"你的主人格：{main_role['name']}")
    st.subheader(main_role["tagline"])
    st.divider()

    # 显示强项和盲区
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("✅ 你的社交强项")
        for s in main_role["strengths"]:
            st.write(f"- {s}")
    with col2:
        st.subheader("⚠️ 你的社交盲区")
        for w in main_role["weaknesses"]:
            st.write(f"- {w}")
    st.divider()

    # 显示当场可用话术
    st.subheader("🎤 当场就能用的开场话术")
    for i, opener in enumerate(main_role["openers"]):
        st.code(f"{i+1}. {opener}", language="text")
    
    # 显示会后跟进模板
    st.subheader("📩 会后跟进邮件模板")
    st.code(main_role["followup"], language="text")
    st.divider()

    # 显示最佳搭子和避雷类型
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🤝 你的最佳会议搭子")
        st.write(main_role["best_match"])
    with col2:
        st.subheader("💥 容易冲突的类型")
        st.write(main_role["conflict_match"])
    
    # 副人格提示
    st.info(f"你的副人格是：{second_role['name']}，你也可以参考它的社交建议哦~")
    st.divider()

    # 重测按钮
    if st.button("重新测试", use_container_width=True):
        # 重置所有状态
        st.session_state.current_question = 0
        st.session_state.user_scores = [0, 0, 0, 0]
        st.session_state.test_finished = False
        st.rerun()