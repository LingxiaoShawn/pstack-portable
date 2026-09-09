# pstack for Codex and Claude Code

把 Lauren Tan 的 [pstack](https://github.com/cursor/plugins/tree/main/pstack)
移植到 Codex 和 Claude Code，保留严谨的工程流程，重点改善代码可维护性和人类交接。

包含上游 47 个主技能、3 个新增入口，以及 1 个运行适配技能。
上游固定为 0.15.0 / `27e2a62ff94f9af4b5e68435e41cdceacadb840c`。
这是独立移植版，不是 Cursor、OpenAI 或 Anthropic 官方发行。

**最快开始**

在这个仓库目录中运行。安装已有生成文件不需要构建，也不需要 PyYAML。
需要 Python 3.10+；实际工程任务需要 Git 和项目自身的开发工具。

Codex，安装到当前用户：

```sh
python3 scripts/install_codex.py
```

然后在 Codex 中使用：

```text
$pstack 完成这个任务，给我简洁的结果和验证依据。
$pstack-refactor 清理这次改动，让后续阅读和修改更容易，保持行为不变。
$pstack-teach 用普通中文和一个真实例子解释这段代码。
$pstack-brief 把最终改动做成大字、少术语的 HTML 讲解。
```

Claude Code，注册本地 marketplace 并安装插件：

```sh
claude plugin marketplace add /absolute/path/to/pstack-portable
claude plugin install pstack@pstack-portable --scope user
```

将上面的绝对路径替换成你的实际仓库位置。打开新会话后使用：

```text
/pstack:poteto-mode 完成这个任务，给我简洁的结果和验证依据。
/pstack:refactor 清理这次改动，让后续阅读和修改更容易，保持行为不变。
/pstack:teach 用普通中文和一个真实例子解释这段代码。
/pstack:brief 把最终改动做成大字、少术语的 HTML 讲解。
```

也可以从仓库目录只试用一次，不注册 marketplace：

```sh
claude --plugin-dir ./claude/plugins/pstack
```

**怎么用最省事**

| 你的目标 | Codex | Claude Code |
| --- | --- | --- |
| 按 pstack 完成工程任务 | `$pstack` | `/pstack:poteto-mode` |
| 清理代码并验证行为 | `$pstack-refactor` | `/pstack:refactor` |
| 做一次轻量去冗余 | `$pstack-deslop` | `/pstack:deslop` |
| 解释代码或改动 | `$pstack-teach` | `/pstack:teach` |
| 生成 HTML 讲解 | `$pstack-brief` | `/pstack:brief` |
| 配置偏好和检查工具 | `$pstack-setup-pstack` | `/pstack:setup-pstack` |
| 评审改动 | `$pstack-interrogate` | `/pstack:interrogate` |

先用默认配置。它继承当前模型，不要求其他厂商的模型或额外 API key。
默认最多两个 worker；客户端不支持或不允许子 agent 时，能够顺序完成的任务由当前 agent 执行。
会明确说明这种退化，不把自查说成独立评审，也不把同模型多次运行说成多模型比较。

`brief` 读取最终代码和验证结果，生成五段 HTML：核心结果、问题、前后结构、真实例子、验证与来源。
它有上一页/下一页、显示全部、打印支持，长内容可以滚动，不使用固定高度裁掉正文。
渲染器本身不判断解释是否真实；事实检查仍要对照代码和实际证据。

**安装、更新和移除**

Codex 默认写入 `~/.agents/skills`，技能名称都以 pstack 开头。
先查看将做哪些操作：

```sh
python3 scripts/install_codex.py --dry-run
```

只安装到一个项目：

```sh
python3 scripts/install_codex.py --project /absolute/path/to/project
```

拉取本仓库更新后，重新运行同一个安装命令。安装器只管理自己的目录，拒绝覆盖同名的其他技能，
也拒绝覆盖你已修改的安装文件。出现本地修改时，先保存并整理这些修改，再更新。

移除用户级安装：

```sh
python3 scripts/install_codex.py --uninstall
```

项目级移除加上相同的 `--project` 参数。不要同时安装用户级和项目级副本，避免重复发现。
也不要同时启用独立技能安装和同一套 Codex marketplace 插件。

Claude Code 更新与卸载使用客户端自己的插件管理：

```sh
claude plugin update pstack@pstack-portable --scope user
claude plugin uninstall pstack@pstack-portable --scope user
```

仓库也提供 `.agents/plugins/marketplace.json` 和 `.codex-plugin/plugin.json`，可用于支持本地
marketplace 的 Codex 界面。默认建议使用上面的独立技能安装路径，覆盖 CLI 和 IDE 使用。

**配置**

配置是可选的。读取顺序是当前项目 `.pstack/config.json`、用户 `~/.config/pstack/config.json`、默认值。
项目文件整体优先，不与用户文件逐字段混合。

```json
{
  "version": 1,
  "max_workers": 2,
  "language": "auto",
  "roles": {}
}
```

`language` 可设为 `zh`。`roles` 只表达 pstack 的偏好，不会修改 Codex/Claude 原生模型配置。
角色名沿用上游，例如 `how explorer`、`architect runners`、`interrogate reviewers`。
单角色可以填 `inherit-parent`；面板可以填不超过 `max_workers` 的列表。
具体模型名必须来自当前客户端实际开放的选项。请求比较某个不可用模型时，不能用别的模型冒充。

不安装也可以检查可选依赖：

```sh
python3 plugins/pstack/skills/pstack-runtime/doctor.py
```

**和上游的差异**

| 内容 | 这个版本的处理 |
| --- | --- |
| Cursor 模型 slug | 默认继承当前模型；只使用目标客户端实际支持的覆盖方式 |
| Cursor Task / cloud 参数 | 使用原生 worker；缺少能力时明确说明，适合时顺序执行 |
| Cursor 的 mode、图标等 frontmatter | 转成各客户端支持的元数据 |
| 上游手动调用策略 | Claude 保留 disable-model-invocation；Codex 转为 openai.yaml 的对应策略 |
| Cursor 插件依赖 deslop | 提供自包含的局部清理实现 |
| control-ui / control-cli | 使用现有浏览器工具或项目命令；缺少验证能力时报告缺口 |
| 聊天记录路径 | 只使用当前项目、客户端或用户明确提供的记录 |
| no-comments 的激进删除 | 保留必要约束、解释原因的注释和不确定的警告 |
| 每次回复列出原则名称 | 直接解释具体选择及效果，避免内部术语泄露到用户交接 |
| 自动开 PR、合并和发送消息 | 只在用户任务或既有授权包含这些操作时执行 |
| Cursor 云调度、循环唤醒、Benny 自动化 | 不作为已移植运行服务；参考源保留在 upstream/ |

完整的覆盖与限制见 [PORTING.md](docs/PORTING.md)。

**验证与开发**

```sh
python3 -m pip install -r requirements-dev.txt
python3 scripts/build.py
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
python3 scripts/build.py --check
```

`upstream/` 是固定版本的参考来源。修改 `overrides/`、`shared/` 或 `scripts/`，然后重新生成两份插件。
不要直接编辑 `plugins/pstack/` 或 `claude/plugins/pstack/`。
构建不访问网络；安装和 brief 渲染只用 Python 标准库。

已验证的检查范围与真实客户端试用步骤见 [VALIDATION.md](docs/VALIDATION.md)。

MIT License。上游版权归 Lauren Tan；保留完整许可和来源记录。
