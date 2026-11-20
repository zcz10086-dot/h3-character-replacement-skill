# 第三方许可与公开发布前检查

核查日期：2026-11-20。完整证据见audit/upstream-plugins.json及audit/workflow-origin.json。公开仓库可见、附带许可证、与本地快照同源，是三个不同的核验问题。

## 来源与许可尚未核实的事项

1. 原分享包人物替换.json及其他工作流：未找到足以证明同一文件GitHub来源和再分发许可的证据。分享来源由本项目维护者确认为“俭朴的AI玩家（抖音号：2191960461）”，该信息不能单独证明原作者身份与许可链。不得用类似工作流仓库或ComfyUI本体GPL代替作者授权。
2. Derfuu_ComfyUI_ModdedNodes：已找到GitHub仓库，但本地包没有完整许可证，本轮常用上游LICENSE路径也未获取到许可正文。pyproject里写“LICENSE”不等于已提供许可。
3. ComfyUI-H3-Conditioning-Cache：本地插件包含MIT LICENSE，但本项目从工作流原包覆盖的正确h3_conditioning_cache.py没有独立来源与许可声明。须确认该覆盖文件属于同一MIT授权范围。
4. Comfyui_Minimax_h3_latent_Upscaler：已获取上游MIT许可证；本地快照缺根LICENSE，公开再分发前应核同源版本并附上原始许可。远程许可原文另存third-party-license-evidence，不默默改旧发布包。

## 来源暂未在GitHub确认

ComfyUI-H3-Conditioning-Cache、ComfyUI-H3-Director保留本地MIT许可证及其中版权人署名；本轮未确认其GitHub项目主页，不编造链接，不把依赖仓库写成自身作者仓库。

## 最终交叉核验

20个插件中，18项找到可网络验证的GitHub来源：14项仓库网页可访问，另4项以仓库raw LICENSE成功读取为证；17项取得远程完整许可证。16项同时存在本地及远程LICENSE的插件，统一换行及首尾空白后全文一致。AIMixer/ComfyUI_MiniMaxH3_Director两端均为Apache-2.0，不能与名称相近的ComfyUI-H3-Director本地MIT混写。latent Upscaler是本地缺许可证、上游存在MIT，不是许可正文冲突。网络核查不能证明整个插件快照逐文件与上游同版本，不能据此省略版本和来源审核。

## 第三方许可保留

MIT项目保留版权与许可证。Apache-2.0项目保留许可证、适用NOTICE及修改声明。GPL项目按原许可分发相应源码与声明。插件vendor、字体、示例、内置资源可能另有许可，完整快照中的嵌套LICENSE/NOTICE同样保留；根许可不能自动覆盖所有资源。

h3-relay除了根GPL还含Apache及vendor许可，见其NOTICE.md/UPSTREAMS.md；WAS包含字体、检测数据和多个vendor组件，不只保留根LICENSE。模型权重不随本项目分发，仍按各模型原条款使用。

## 发布状态

旧版 Skill 为流程工具包；新版 Skill 和独立工作流插件 ZIP 按维护者要求保留全部配套材料及原有许可证。目前远端仓库已创建，GitHub 写入权限已恢复，源码正在分批发布；Release 二进制附件尚待发布。以上待核实事项如实保留；本项目自有代码的 GPL-3.0-only 许可不替代第三方授权，也不宣称这些事项已经解决。
