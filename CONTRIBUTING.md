# FiberTree 贡献指南

感谢您对FiberTree项目的关注！我们欢迎任何形式的贡献，无论是代码贡献、文档改进、问题报告还是功能建议。本指南将帮助您了解如何有效地参与项目。

## 行为准则

参与本项目的所有贡献者都应该尊重彼此，保持友好和建设性的交流。我们希望创建一个包容和支持的环境，让每个人都能自由地分享想法和贡献。

## 如何贡献

### 报告问题

如果您在使用FiberTree时遇到问题，或者有改进建议，请通过GitHub Issues报告。创建问题时，请：

1. 使用清晰、具体的标题
2. 提供详细的问题描述
3. 包含复现步骤（如适用）
4. 描述预期行为和实际行为
5. 提供环境信息（操作系统、Python版本等）
6. 如果可能，附上相关代码片段或错误日志

### 提交拉取请求

如果您想贡献代码或文档，可以通过以下步骤提交拉取请求（Pull Request）：

1. Fork本仓库
2. 创建您的特性分支：`git checkout -b feature/your-feature-name`
3. 提交您的更改：`git commit -m 'Add some feature'`
4. 推送到您的分支：`git push origin feature/your-feature-name`
5. 提交拉取请求到我们的`main`分支

### 编码规范

为保持代码库的一致性，请遵循以下编码规范：

- 遵循[PEP 8](https://www.python.org/dev/peps/pep-0008/)Python代码风格指南
- 使用4个空格缩进（不使用制表符）
- 所有新代码必须包含适当的类型提示
- 每个公共函数、类和方法必须有文档字符串
- 确保您的代码通过所有现有测试
- 为您添加的新功能编写测试

### 文档贡献

文档改进是非常重要的贡献形式。您可以：

- 改进现有文档
- 添加更多示例和教程
- 修正文档中的错误或过时信息
- 改进文档的结构和可读性

## 开发环境设置

以下是设置本地开发环境的步骤：

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/fbtree.git
cd fbtree
```

2. 创建并激活虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # 在Windows上使用 venv\Scripts\activate
```

3. 安装开发依赖：
```bash
pip install -e ".[dev]"
```

4. 安装预提交钩子：
```bash
pre-commit install
```

## 测试

在提交拉取请求前，请确保您的代码通过所有测试：

```bash
pytest
```

对于添加的新功能，请编写相应的测试。我们使用`pytest`作为测试框架。

## 版本控制

我们使用[语义化版本控制](https://semver.org/)。版本号格式为：`主版本.次版本.修订号`。

- 主版本号：不兼容的API变更
- 次版本号：向后兼容的功能性新增
- 修订号：向后兼容的问题修正

## 项目结构

以下是项目的主要目录结构：

```
fbtree/
├── core/           # 核心功能模块
├── storage/        # 存储后端实现
├── analysis/       # 分析功能
├── utils/          # 实用工具
├── visualization/  # 可视化功能
tests/              # 测试用例
examples/           # 使用示例
docs/               # 文档
```

## 发布流程

项目维护者会定期发布新版本。发布流程如下：

1. 更新版本号在`setup.py`中
2. 更新`CHANGELOG.md`
3. 创建一个新的版本标签
4. 构建并上传到PyPI

## 联系我们

如果您有任何问题或需要帮助，可以通过以下方式联系我们：

- 在GitHub上提交Issue
- 发送邮件至[项目维护者邮箱]

再次感谢您对FiberTree项目的贡献！ 