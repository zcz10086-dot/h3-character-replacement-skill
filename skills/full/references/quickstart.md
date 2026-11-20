# 使用入口

安装目录为用户级skills/h3-character-replacement，SKILL.md由助手匹配任务时加载。直接告诉助手：

“使用h3-character-replacement，先检查我提供的官方包、原视频、人物参考和SSH，输出部署与资产检查结果；不要擅自改变官方工作流。”

“用这个Skill处理我已确认范围的字幕/水印，先做短样本和连续帧验收，再切镜头。”

“继续这个项目的H3双采批量生产，先对账已有receipt/history/output/cache，成功视频及时下载。”

“检查合片是否有长停帧，按原帧序和原声重建，不重跑人物替换。”

## 手工运行

使用你实际验证过的Python解释器；本机现有ComfyUI虚拟环境曾通过全部本地依赖测试，但这不是要求新机器沿用某个用户路径。脚本不会自动安装缺失组件。

```text
python scripts/project_check.py YOUR_PROJECT_CONFIG.json --report NEW_CHECK.json
python scripts/test_guards.py
python scripts/video_pipeline.py --help
python scripts/test_video_pipeline.py --report NEW_VIDEO_TESTS.json
python scripts/cloud_runtime.py --help
python scripts/comfy_batch.py --help
```

命令在Skill目录运行，或将scripts路径替换成Skill绝对路径。视频需要已有cv2/numpy/imageio-ffmpeg和ffprobe；SSH需要已有paramiko。网络工具只在明确调用远程动作时连接，--help不连接。

## 阅读顺序

1. tutorial.md：从原片到交付完整流程。
2. video-and-assets.md、asset-review.md：字幕水印、帧映射、参考人物与mask。
3. cloud-and-production.md、assets/models.json：服务器环境、节点、模型、批量账本。
4. acceptance.md：官方模板保护和真实视觉门禁。
5. troubleshooting.md：本次真实踩坑与恢复方式。
6. test-report.md、video-tests.json、cloud-tests.json：精确测试范围。

官方工作流原包、人物替换画布、成功一采/二采API模板和完整20插件归档现已随assets/runtime附带，先读runtime-bundle.md并执行python scripts/verify_runtime.py。模型大权重、ComfyUI本体和私人素材不在本包内；ComfyUI按教程固定v0.46.0，权重按assets/models.json下载校验。插件上游内置的小型资源和示例保留完整。当前Skill仍需实际素材、目标环境依赖安装及人工验收，不能仅凭文件齐全宣布GPU生产通过。
