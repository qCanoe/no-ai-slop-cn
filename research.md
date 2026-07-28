# 研究依据与设计边界

本文件记录 No AI Slop 中文版 1.1.0 的资料来源和取舍。它不是“AI 文本检测器”的技术说明，也不主张仅凭文风判断作者身份。

## 结论先行

1. **没有可靠的单词级身份证。** “此外”“不是……而是……”或破折号都可能出现在自然人类写作中。研究更常观察词汇分布、句法结构、篇章推进和多项特征的组合差异。
2. **模型、领域和时间会改变特征。** 某个模型在问答、论文摘要或社交文案中的统计差异，不能直接推广到所有中文文本。
3. **本项目处理可观察的写作问题，不判断作者。** “空泛、虚高、模板化、来源不明、结构重复”本身就值得编辑，无论文本由谁写成。
4. **保留事实和文体比去痕更重要。** 正式、学术、技术和法律文本天然更规范；规范、平实或中性不等于 AI 腔。
5. **单点提示弱，模式聚类强。** 同一篇文本同时出现重要性吹捧、模糊归因、三段式、通用积极结尾和聊天助手残留时，才构成更有意义的编辑证据。

## 研究如何进入规则

- 中文开放域问答研究比较了描述性特征、字词常用度、字词多样性、句法复杂性和语篇凝聚力。本项目据此避免把“禁词命中”当作唯一判断。
- 关于 AI 生成文本语言特征的综述讨论了重复、词汇多样性、名词比例、较正式或非人格化的表达，以及句法与话语标记差异。本项目据此采用分层扫描和上下文判断；“去名词化”主要来自中文清晰写作实践，不作为该综述直接证明的 AI 特征。
- QUDsim 研究关注大模型反复使用相似篇章结构的问题，本项目据此强化“段落同构”检查。“列表膨胀”和“挑战与展望”来自编辑实践与多个开源项目的重复观察，不归因于该研究。
- 依存句法研究显示，中文模型文本中的话语标记、并列关系和标点组合可能具有区分作用。本项目只把这些视为弱提示，要求与其他模式共同出现。
- 中文技术写作规范强调清晰、简洁、一致、明确指代和稳定术语。本项目将这些作为基础质量要求，不把它们说成 AI 证据。
- 国家标准用于处理明显标点和数字体例问题。本项目不会为了追求排版统一破坏文学、品牌或项目既有风格。

## 学术与实证资料

1. 朱君辉等：《人工智能生成语言与人类语言对比研究——以 ChatGPT 为例》，CCL 2023。  
   https://aclanthology.org/2023.ccl-1.46/
2. *Linguistic Characteristics of AI-Generated Text: A Survey*（arXiv 预印本）。  
   https://arxiv.org/abs/2510.05136
3. *QUDsim: Quantifying Discourse Similarities in LLM-Generated Text*（OpenReview 论文页面）。  
   https://openreview.net/forum?id=zFz1BJu211
4. *DependencyAI: Detecting AI Generated Text through Dependency Parsing*（arXiv 预印本）。  
   https://arxiv.org/abs/2602.15514
5. 《国内外大语言模型生成中文论文摘要对比研究——以图书情报领域为例》。  
   https://www.kmf.ac.cn/CN/10.13266/j.issn.2095-5472.2024.032
6. *Linguistic features of AI mis/disinformation and the detection limits of LLMs*。  
   https://pmc.ncbi.nlm.nih.gov/articles/PMC12800167/
7. *CAT-LLM: Style-enhanced Large Language Models with Text Style Definition for Chinese Article-style Transfer*（arXiv 预印本）。  
   https://arxiv.org/abs/2401.05707

这些研究的任务、语料和模型不同，结论不能直接当作通用检测规则。本项目只吸收可解释、能改善文本、且有明确误判边界的部分。

## 中文规范与编辑指南

1. 全国标准信息公共服务平台：GB/T 15834—2011《标点符号用法》。  
   https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=22EA6D162E4110E752259661E1A0D0A8
2. 全国标准信息公共服务平台：GB/T 15835—2011《出版物上数字用法》。  
   https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=F5DAC3377DA99C8D78AE66735B6359C7
3. MDN Web 文档项目：《文档写作规范》。  
   https://developer.mozilla.org/zh-CN/docs/MDN/Writing_guidelines/Writing_style_guide
4. 《中文技术文档写作风格指南》。  
   https://zh-style-guide.readthedocs.io/zh-cn/latest/
5. 阮一峰：《中文技术文档的写作规范》。  
   https://github.com/ruanyf/document-style-guide
6. 清华大学经济管理学院：《研究生学位论文写作指南》。  
   http://mis.sem.tsinghua.edu.cn/ueditor/jsp/upload/file/20231121/1700565210223040873.pdf

## 开源项目与社区观察

以下项目用于比较规则覆盖、工作流和误判保护。本项目没有把它们当作学术证据，也没有复制其大段文本。

1. Peter Yang：`no-ai-slop`，本项目的结构与核心工作流来源。  
   https://github.com/petergyang/no-ai-slop
2. Siqi Chen：`humanizer`。  
   https://github.com/blader/humanizer
3. `Humanizer-zh`。  
   https://github.com/op7418/Humanizer-zh
4. `humanizer-zh-next`。  
   https://github.com/Hyacehila/humanizer-zh-next
5. `zh-writing-humanizer`。  
   https://github.com/ruijayfeng/zh-writing-humanizer
6. `remove-ai-flavor-writing-skill`。  
   https://github.com/B1lli/remove-ai-flavor-writing-skill
7. `qu-ai-wei`。  
   https://github.com/899ms/qu-ai-wei
8. `stop-slop-zh`。  
   https://github.com/leeguooooo/stop-slop-zh
9. 维基百科：《AI 生成文的特征》。  
   https://zh.wikipedia.org/wiki/Wikipedia:AI生成文的特徵

## 明确不采用的做法

- 不提供“像人概率”“AI 率”或规避学校、期刊、平台检测器的承诺。
- 不通过随机插入口语、错别字、反问、第一人称或情绪制造假人味。
- 不要求文章必须长短句交错、必须删光连接词或必须避开所有四字词。
- 不把正式、完整、中立、语法正确本身视为问题。
- 不为增加具体感而虚构数字、场景、经历、引语或来源。
- 不默认模仿具体作者；用户样文只用于校准其本人的可观察语言习惯。

## 维护规则

新增模式至少应满足以下条件之一：

1. 有研究或权威写作规范支持；
2. 在多个模型、多个文本或多个独立社区观察中重复出现；
3. 即使与 AI 无关，处理后也能稳定提高中文表达质量。

每条新规则必须同时写明修法和误判边界，并在 `tests.md` 添加正向与反向用例。
