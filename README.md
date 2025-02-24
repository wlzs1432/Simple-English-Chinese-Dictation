# 🎧 简易中英听写器 (Simple English-Chinese Dictation)

一个简单的英语听写练习工具，支持分类管理单词、测试题生成，并基于 SQLite 进行数据存储。

---

## ✨ 功能特色

- 📂 **类别管理**：支持创建单词类别，便于分类学习。
- 📝 **单词管理**：在类别下添加、删除单词
- 🏆 **测试模式**：可以选择类别生成测试题，并逐题弹出进行练习。
- 🔄 **数据存储**：使用 SQLite 数据库管理单词，支持持久化存储。
- 🌐 **界面交互**：基于 Tkinter 图形界面，提供直观的用户体验。

---

## 🎮 使用说明

### 📂 **1. 添加类别**

- 在主界面点击 **"添加类别"** 按钮。
- 输入类别名称（例如 **"2025-02-23 单词"**）。
- 点击 **"确认"**，类别将添加到主界面。

### 📜 **2. 查看类别**

- 在主界面，点击已创建的类别名称。
- 进入类别详情页面，可查看该类别中的所有单词。

### ✏️ **3. 添加单词**

- 进入某个类别后，点击 **"添加单词"** 按钮。
- 输入英文单词，并提供相应的中文释义。
- 点击 **"确认"**，单词会添加到当前类别。

### ❌ **4. 删除单词**

- 在类别详情页面，每个单词旁边有 **"删除"** 按钮。
- 点击即可删除该单词。
- 也可点击 **"清空类别"** 删除该类别下的所有单词。

### 🔄 **5. 刷新列表**

- 在类别详情页面点击 **"刷新"** 按钮，确保刚添加的单词及时显示。

### 📋 **6. 生成测试题**

- 在主界面点击 **"生成测试题"** 按钮。
- 选择要测试的类别，并选择题目数量。
- **题目将逐题弹出**，用户输入答案后，系统会检查正确性。

## 🔮 未来计划

- 🌍 Web 版
- 🗣️ 语音朗读
- 📚 离线词典
- 🌐 更好的交互界面

## 📜 许可证

本项目采用 MIT 许可证，详情请查看 `LICENSE`。

------

## 🤝 贡献指南

如果你有兴趣贡献代码或提出建议，欢迎提交 PR 或 issue！🎉