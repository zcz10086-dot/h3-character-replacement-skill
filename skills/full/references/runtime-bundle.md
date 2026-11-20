# 完整工作流与插件材料

本补全版把本项目实际使用的官方工作流和配套插件装进Skill，路径均相对Skill根目录。仅提供材料，不向本机ComfyUI自动安装插件，也不启动云服务。

## 物料入口

- `assets/runtime/official-workflows.zip`：官方MiniMax-h3工作流原包，保留全部工作流和原包Python文件。原包中的备份不等于推荐部署版本。
- `assets/runtime/workflows/人物替换.json`：官方人物替换画布原样副本，SHA256应为`af38fd413d948c8fcdc4e67856822ff5f35f789d9706475f0f8c10f67f1e5304`。在ComfyUI界面导入该文件；不要把画布直接提交API。
- `assets/runtime/workflows/stage1.api.json`、`stage2.api.json`：实际成功的一采77节点、二采62节点API模板。最终视频节点分别为1349、1247。仅将实例素材路径、输出隔离字符串和人物提示泛化，结构、数值与连接保持不变；变更审计及可改字段见同目录文件和manifest。
- `assets/runtime/workflows/mask.api.json`：历史成功SAM3遮罩API示例，保留7节点完整图；使用people文本提示及原阈值/max_objects等参数，无手工点位。参数仍来自旧小样，必须按新素材重新审核并建立批准版本，不能把旧配置当通用遮罩。
- `assets/runtime/plugins-production.zip`：生产插件完整快照，20个顶层插件目录，保留源码、前端、requirements、许可证、上游示例及内置资源。不是仅摘几份Python文件。
- `assets/runtime/deploy-plugins.steps.json`：插件安全解包、20个具体目录归位及真实根requirements安装步骤，供合并进cloud.json；使用前检查其路径与主部署配置一致。
- `assets/runtime/overrides/h3_conditioning_cache.py`：实际成功部署的正确缓存源码，SHA256 `763c6a6b4da82e4f7c6aa70426b1c6845860e870ad0569091c9e5668807d2d4a`。生产插件zip已内置该版本，避免再次覆盖旧版。
- `assets/runtime/manifest.json`：物料及归档每个成员的大小、SHA256、插件目录、来源与变更记录。
- `assets/runtime/node-coverage.json`：API与画布节点来源的静态核查记录。画布中UUID类型属于随画布保存的子图定义；前端Set/Get、组旁路节点也要保留相应插件前端。静态覆盖没有明确缺项，不等于已在全新v0.46.0云机执行全部节点。

完整插件目录：h3-relay、ComfyUI-H3-Motion-Context、ComfyUI-H3-Conditioning-Cache、ComfyUI-H3-FaceRefine、ComfyUI-MiniMaxH3Mod、ComfyUI-H3-Director、ComfyUI_MiniMaxH3_Director、ComfyUI-Image-Oasis、ComfyUI-noEmbryo、Veda-on-ComfyUI、ComfyUI-VideoHelperSuite、ComfyUI-Easy-Use、ComfyUI_essentials、Derfuu_ComfyUI_ModdedNodes、rgthree-comfy、was-node-suite-comfyui、ComfyUI-KJNodes、ComfyMath、Comfyui_Minimax_h3_latent_Upscaler、resolution-selector-live。

其中插件自带examples图片/视频、字体、级联检测数据和少量小型safetensors属于上游资源，保留以保证插件完整，不是本项目私人素材。九项H3生产大模型仍通过assets/models.json下载校验。

## 本地完整性核验

```text
python scripts/verify_runtime.py
python scripts/test_guards.py
```

核验工具不导入插件、不联网、不安装。它读取manifest，逐物料及归档成员核验大小/hash，检查CRC和越界/符号链接，确认双采节点数及正确缓存文件。通过只表示物料与清单一致，不表示目标机器全部节点能运行。

## 部署顺序

1. 固定ComfyUI v0.46.0，按cloud-and-production.md准备Python、torch/CUDA与core requirements。SAM3_VideoTrack/SAM3_TrackToMask来自该版core，不能另装同名替代。
2. 核验本包，把plugins-production.zip安全解压至暂存目录；20个顶层目录分别放入新的ComfyUI/custom_nodes。优先新运行目录，已有同名插件先核版本、备份并处理冲突，不能盲覆盖用户环境。
3. 为实际插件安装其requirements及历史补充依赖，详见云部署教程。deploy-plugins.steps.json是需人工合并的步骤片段，不含SSH或ComfyUI基础安装；其中插件归档SHA已填写，上传local路径和cloud.json的remote_root仍按当前项目设置。源码完整不代表第三方Python依赖已安装；不要为了少数示例功能无限扩装环境。
4. 模型逐项SHA256通过；启动受管ComfyUI并核/object_info。逐个核API的class_type及输入schema，特别是conditioning的STRING接口和循环节点。
5. 在界面导入原始画布。生产使用附带API模板，通过prepare_payload.py更换明确白名单字符串。先实际验证一段小样、模型加载和SAM3分支，再进入批量。

API模板里的Picture1/2/3输入次序固定。示例提示不能替代新镜头身份审核，路径、人物、输出缓存必须按新项目填写。数字帧数/分辨率/种子等保持原样，确需改变时应建立新批准模板并重新验证，不能以路径替换工具偷偷改数字。

## 来源、许可与验证边界

附带第三方插件原有LICENSE/NOTICE等文件，不改变原许可。官方工作流原包未见单独许可证，本包保留原文件但不声称额外授予再分发权；再次公开发布时由发布者核对各原作者条款。完整性清单不是软件供应链安全审计。

本轮补全仅本地材料核对与回归，不连接云机、不修改本机ComfyUI、不下载大模型、不执行GPU采样。原流程历史成功与本补全版新机验证是不同事实。ComfyUI本体、Python/CUDA二进制、依赖wheel和九项大权重未塞进skill，仍需要按固定版本在目标机器安装。不能承诺断网机器仅凭本包完成全环境部署。
