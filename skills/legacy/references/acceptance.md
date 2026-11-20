# 验收记录与门禁

## 项目配置

`assets/project.example.json`是描述项目的主模板，独立工具使用的细分配置以其各自--help和教程为准，不保证一个配置文件能原样传入所有工具。

`python scripts/project_check.py PROJECT.json --report project_check.json`检查Picture唯一固定索引、参考文件、原/清理片存在、镜头半开区间连续、总覆盖帧数、原段保留原因、字幕水印策略已审核、默认90/match。它不自动识别画面身份，也不验证用户是否确实看过素材。

shot示例：

```json
{"id":"SHOT_00","start":0,"end":120,"roles":["P2","P3"],"screen_binding":{"left":"P2","right":"P3"},"preserve_original":false}
```

## 工作流差异

```text
python scripts/workflow_guard.py APPROVED_API.json CANDIDATE_API.json --allow NODE.input_field --report diff.json
```

白名单必须来自该项目批准的路径/提示文本/输出字段，不能为了通过检查而自动允许所有字符串，更不能允许任意数字或连接变化。画布校验可同时提供--canvas和--canvas-sha256。比较器保护节点、class_type、inputs字段和非字符串值，API包装中的client_id等不作为图输入。UI元数据不等于执行结构。

## 从官方模板生成项目载荷

`python scripts/prepare_payload.py --template APPROVED_API.json --replacements STRINGS.json --output NEW_PAYLOAD.json --report NEW_DIFF.json`。STRINGS.json是明确的 `node.input` 到新字符串的JSON对象，例如输入图/视频路径、prompt和隔离输出名；节点编号来自实际模板，不从示例硬套。只允许替换已存在的字符串字段，不能更改数值、连线或节点，输出必须是新文件。报告含模板SHA256和允许变更字段。替换配置由审图后的镜头绑定生成；本工具不自动猜人物或遮罩。

## 视觉pass

```json
{"approved":true,"revision":"r1","stage":1,"prompt_id":"ACTUAL_PROMPT_ID","reviewer":"actual reviewer","evidence":["absolute/path/contact.jpg"],"reviewed_frames":[0,1,2,87,88,89,90,91],"checks":{"identity":"pass","face":"pass","clothing":"pass","occlusion":"pass","source_actor_residue":"pass","lip_motion":"user accepted"},"scope":"key frame and boundary sampling, not exhaustive frame-by-frame visual certification"}
```

真实审图后写入，不从history status自动推导；不沿用其它revision/prompt_id的pass。批量工具更严格的字段格式以其说明为准，概念上必须关联实际任务。

## 每次提交前

原图哈希、Picture索引、source/mask有效帧、遮罩首中尾与跨窗、具体左右身份、官方差异批准、缓存输出隔离、已对账无重复intent。stage2额外核同一revision的stage1真实visual_pass和conditioning/latent完整性。

## 成片

1. 用最终文件实际解码到EOF，核每镜头和全片帧数。
2. 核PTS等间隔、packet duration、窗口切换与末帧；重建时间轴后每个有效源帧映射可追溯。
3. 映射原全片音轨；copy时核包hash和PTS/DTS，重编码时核波形最佳偏移及采样长度。容器AAC边界多约毫秒不能误判音画错位。
4. 全片近重复run筛选；记录分辨率、MAD阈值、黑场例外、与原片静态区对照。仅像素小差异不代表真实运动，不能把重复run全自动当错误。
5. 重点边界连续帧、所有返修点、动作时间及口型用户接受范围。对照原片和最终文件，不只比较错误中间片与最终片。
6. 交付另存成片与关键短片，报告精确检查和未覆盖范围。
