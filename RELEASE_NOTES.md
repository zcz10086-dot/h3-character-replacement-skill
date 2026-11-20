# H3 Character Replacement Skill 发布材料

目标仓库：https://github.com/zcz10086-dot/h3-character-replacement-skill 。仓库已创建，GitHub 写入权限已恢复；源码正在分批发布至 main 分支，Release 二进制附件尚待发布。

## 附件

- h3-character-replacement-legacy.skill：旧版流程工具包，67,643 字节，21 个文件。
- h3-character-replacement-full.skill：完整工作流插件版，127,697,866 字节，37 个文件。
- comfyui-workflows-and-plugins.zip：独立工作流插件材料，127,622,928 字节，14 个顶层材料文件。
- SHA256SUMS.txt：上述三个附件的 SHA256。

两个 Skill 已将教程中的本机用户名路径改为通用示例，保持安装根目录 h3-character-replacement。工作流和插件材料完整保留。两个大附件超过普通 Git 的 100 MiB 单文件限制，计划作为 Release 附件分发；附件尚待另行发布，本次源码上传不包含二进制附件。

## 包含内容

字幕水印预处理、人物资产与遮罩、SSH 云环境准备、九模型下载校验、工作流结构保护、一采二采批量下载和视觉验收、按实际帧序排查停帧及原声合片。

完整材料版含 242 节点原画布、77/62 节点双采 API、7 节点 SAM3 示例、20 插件共 2912 成员的完整快照、正确缓存源码、部署步骤与文件校验清单。数值和连接不因素材路径泛化而改变。

## 校验与许可

两个 Skill 均通过 Skill 元数据校验，三个附件 CRC 校验通过，已更新 SHA256。第三方来源、许可证和待核实事项保留在 THIRD_PARTY_NOTICES.md 及 audit 目录，不将项目自身 GPL-3.0-only 许可套用于所有第三方材料。

本轮没有进行新云机重部署或 GPU 重采样；原有测试范围见各版本 references/test-report.md。
