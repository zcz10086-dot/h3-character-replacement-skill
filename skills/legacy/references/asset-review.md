# 人物资产与遮罩制作操作卡

## 参考图与身份表

每个人物指定不可重用的identity和1-based Picture索引，记录原图路径与SHA256。参考图应看清脸、发型、眼镜与目标服装，尽量包含所需全身区域；不凭长发/年龄/站位重新编号。裁切、放大或拼参考版须记录生成方式和检查，不把模糊原图增强结果当真实细节。

每个镜头先看源连续画面，写角色出场人数和屏幕位置，含转身、出入画、遮挡和转场两侧。prompt不改固定Picture索引。示例仅示范绑定逻辑：`Replace the left visible person with <Picture 2> and the right visible person with <Picture 3>. Match each assigned picture for face, hair and clothing. Preserve movement, camera and scene.` 实际Video标签编号必须查当前官方节点的1-based规则与参考连接，不盲用Video0。

## 人物mask与字幕mask分开

- 人物mask用于H3 edit mask，覆盖目标人物头发、脸、耳、脖子、领、肩衣及实际需要替换的身体，不默认包含被人物挡住的背景。
- 字幕/水印mask用于清理源片，覆盖经确认的文字像素与描边。先清理并选定唯一clean_source，再切段/做人物mask。
- 前景道具、货架、他人手臂和透明转场须分别审核，不能把mask闭运算当万能补齐。

## 使用已有SAM3环境

确认用户授权部署范围和已有SAM3插件、模型及API object_info。按照该版本节点schema生成prompt/mask请求，使用已验证的文本/点/框追踪配置；不同版本节点名和输入字段不同，不凭本卡猜节点JSON。首次导出成功API请求作为项目sam_mask_template并保存版本/hash，后续只改被批准的输入路径和明确提示。

输入必须为真实执行source，提交前核总帧、尺寸、fps。结果下载后核mask实际帧数、二值性和每帧覆盖变化；源+红mask叠图首中尾、窗口边界、快速运动和出入画连续帧人工看。若尚无SAM3模板，先在当前UI/节点schema完成一个短样本，不将它包装成“通用节点结构已验证”。

## 必要修补

局部单帧漏区可借相邻帧轮廓/光流候选，但候选必须对照当前真实source，不能直接跨帧套固定多边形。小孔填充、闭运算只在审定人物区域，避免背景缝、手指间、前景物件被吞。对修订保存：改变的帧索引、mask新增/移除像素、源有效帧逐像素一致、其余mask帧逐像素一致。原文件不覆盖。

单帧整人漏mask会产生“衣服一部分已换、脸与原领口仍在”；只看均匀8帧采样可能漏检，连续首帧和每窗口起点必须看。最终由生成视觉验收决定是否真正通过，不把完整mask等同无原演员残留。

## 转场上下文

若原镜头开头已在交叉溶解中间，先看真实前一镜和当前mask。明确授权后可前接真实prefix，保存prefix_frames、original_frames及逐像素一致证据，prompt按当前画面条件绑定，避免每90窗重置故事先后。生成后先验全部窗口、再只trim新增prefix。trim是非幂等操作，须标记已裁且保留raw记录，禁止对已裁结果重复执行。
