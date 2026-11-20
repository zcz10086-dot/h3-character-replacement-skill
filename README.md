# H3 人物替换 Skill

把一段视频里的人物换成指定角色，保留原来的动作、场景和声音。

这个项目是做完一条多人替换视频后整理出来的。部署环境、处理字幕水印、做人物遮罩、分段生成、最后拼回完整视频，这些步骤都写进了 Skill；中途遇到的串人、漏罩、缓存不兼容和合片停帧，也留下了排查方法。

适合用支持 Skill、能执行 Python 和 SSH 的 AI 助手来跑。视频生成使用 ComfyUI 和 MiniMax H3。

[版本选择](#版本选择) · [开始使用](#开始使用) · [详细教程](#文档) · [致谢](#致谢)

## 能做什么

- 通过 SSH 检查云算力环境，部署 ComfyUI、插件和模型。
- 处理软字幕，以及指定区域的硬字幕、水印；复杂背景需要另外做修复测试。
- 按镜头切片，整理人物参考图和遮罩，固定各角色的 Picture 对应关系。
- 批量运行一采、二采，生成成功后及时下载，断线后对账续跑。
- 检查人物、衣服和遮挡；按实际帧序合片，保留完整原声，排查异常停帧。

## 版本选择

| 文件 | 包含内容 | 怎么选 |
| --- | --- | --- |
| `h3-character-replacement-legacy.skill` | 教程、配置示例和辅助脚本 | 已有工作流和插件，选这个 |
| `h3-character-replacement-full.skill` | 旧版内容，加工作流、双采及遮罩 API、20 个插件的完整快照 | 需要一起准备工作流和插件，选这个 |
| `comfyui-workflows-and-plugins.zip` | 单独的工作流、插件、部署步骤和文件校验清单 | 只需要配套材料，选这个 |

源码正在发布至本仓库；三个附件已在本地整理，尚待发布至 GitHub Releases。完整包保留全部配套工作流和 20 个插件，来源与许可证核查见[第三方说明](THIRD_PARTY_NOTICES.md)。

两个 Skill 安装一个即可，加载名称都是 `h3-character-replacement`。包内不含 ComfyUI 本体、Python/CUDA 环境和大模型权重；这些按教程在目标机器上安装，九项模型约 43.8 GiB。

## 开始使用

### 1. 安装 Skill

将选定的 `.skill` 导入你使用的助手。如果工具采用目录形式加载 Skill，解压后把 `h3-character-replacement` 文件夹放进对应的 skills 目录。

完整包中的插件先按部署说明检查和安装，单纯导入 Skill 不会自动把插件装进 ComfyUI。

### 2. 准备素材

准备好原视频、每个角色的参考图，以及云算力的 SSH 连接信息。多人视频先确定谁对应 Picture 1、Picture 2、Picture 3，再按镜头确认人物位置。

可以这样开始：

```text
使用 h3-character-replacement。
我准备了一段视频和三张人物参考图，先检查素材和云算力环境。
需要处理底部字幕，先做一个短样本让我看效果。
```

凭据单独配置，别写进工作流、提示词或仓库。

### 3. 先跑一个镜头

选一个有代表性的镜头，检查参考图、遮罩和一采效果。脸、衣服、身份和遮挡没问题，再跑二采、扩大到其他镜头。

后续可以直接说：

```text
继续这个项目。先核对已有任务和缓存，不要重复提交。
已通过检查的镜头继续二采，成功后马上下载。
```

最后按原片的镜头帧数拼回去，使用原片完整音轨。具体命令和配置见下面的教程。

## 文档

- [完整制作流程](skills/full/references/tutorial.md)
- [云环境部署与批量生产](skills/full/references/cloud-and-production.md)
- [字幕、水印与视频处理](skills/full/references/video-and-assets.md)
- [人物参考与遮罩](skills/full/references/asset-review.md)
- [工作流和插件包说明](skills/full/references/runtime-bundle.md)
- [常见问题与踩坑记录](skills/full/references/troubleshooting.md)
- [测试记录](skills/full/references/test-report.md)

这些脚本做过本地回归和真实停帧样本测试；封装后没有在一台新云机上重新跑完整套 GPU 生产。换环境后仍要先跑小样，生成任务显示成功也要看实际画面。

## 致谢

感谢 **俭朴的AI玩家（抖音号：2191960461）** 的资料分享。

感谢 **[linux.do 社区](https://linux.do/)** 的交流与分享。

## 许可证

本项目编写的脚本和教程采用 [GPL-3.0](LICENSE)。第三方工作流、插件和模型保留各自许可，详见[第三方说明](THIRD_PARTY_NOTICES.md)。
