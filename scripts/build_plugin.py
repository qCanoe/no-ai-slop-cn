#!/usr/bin/env python3
"""构建并校验可分发的 No AI Slop 中文版插件压缩包。"""

from __future__ import annotations

import argparse
import json
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / ".codex-plugin" / "plugin.json"
DIST = ROOT / "dist"
SKILL_FILES = ("SKILL.md", "eval.md", "research.md", "tests.md")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="执行校验，但不保留构建产物",
    )
    return parser.parse_args()


def validate_source(manifest: dict) -> None:
    required = ("name", "version", "description", "author", "skills", "interface")
    missing = [key for key in required if not manifest.get(key)]
    if missing:
        raise SystemExit(f"插件清单缺少字段：{', '.join(missing)}")

    interface = manifest["interface"]
    interface_required = (
        "displayName",
        "shortDescription",
        "longDescription",
        "developerName",
        "category",
        "capabilities",
        "defaultPrompt",
    )
    missing_interface = [
        key for key in interface_required if not interface.get(key)
    ]
    if missing_interface:
        raise SystemExit(
            f"插件界面配置缺少字段：{', '.join(missing_interface)}"
        )

    prompts = interface["defaultPrompt"]
    if len(prompts) > 3 or any(len(prompt) > 128 for prompt in prompts):
        raise SystemExit(
            "初始提示最多三条，每条不得超过 128 个字符"
        )

    for source in (
        *(ROOT / name for name in SKILL_FILES),
        ROOT / "agents" / "openai.yaml",
        ROOT / "assets" / "no-ai-slop-cn.png",
        ROOT / "LICENSE",
        ROOT / "PRIVACY.md",
        ROOT / "TERMS.md",
    ):
        if not source.is_file():
            raise SystemExit(f"缺少插件源文件：{source.relative_to(ROOT)}")

    skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    if len(skill_text.splitlines()) >= 500:
        raise SystemExit("SKILL.md 必须少于 500 行")
    if not skill_text.startswith("---\nname: no-ai-slop-cn\n"):
        raise SystemExit("SKILL.md 的名称或 YAML 前置信息无效")
    if f'version: "{manifest["version"]}"' not in skill_text:
        raise SystemExit("SKILL.md 与插件清单的版本号不一致")
    for reference in ("[research.md](research.md)", "[tests.md](tests.md)"):
        if reference not in skill_text:
            raise SystemExit(f"SKILL.md 未引用配套文件：{reference}")

    tests_text = (ROOT / "tests.md").read_text(encoding="utf-8")
    missing_cases = [
        heading
        for heading in (
            *(f"### {number}." for number in range(1, 31)),
            *(f"### R{number}." for number in range(1, 9)),
        )
        if heading not in tests_text
    ]
    if missing_cases:
        raise SystemExit(f"回归测试缺少用例：{', '.join(missing_cases)}")

    research_text = (ROOT / "research.md").read_text(encoding="utf-8")
    if research_text.count("https://") < 10:
        raise SystemExit("research.md 至少需要十个可核对的来源链接")


def build_plugin(manifest: dict) -> tuple[Path, Path]:
    plugin_root = DIST / "no-ai-slop-cn"
    if plugin_root.exists():
        shutil.rmtree(plugin_root)

    skill_root = plugin_root / "skills" / "no-ai-slop-cn"
    (plugin_root / ".codex-plugin").mkdir(parents=True)
    (plugin_root / "assets").mkdir(parents=True)
    skill_root.mkdir(parents=True)
    (skill_root / "agents").mkdir()

    shutil.copy2(MANIFEST, plugin_root / ".codex-plugin" / "plugin.json")
    for name in SKILL_FILES:
        shutil.copy2(ROOT / name, skill_root / name)
    shutil.copy2(
        ROOT / "agents" / "openai.yaml",
        skill_root / "agents" / "openai.yaml",
    )
    shutil.copy2(
        ROOT / "assets" / "no-ai-slop-cn.png",
        plugin_root / "assets" / "no-ai-slop-cn.png",
    )
    shutil.copy2(ROOT / "LICENSE", plugin_root / "LICENSE")
    shutil.copy2(ROOT / "PRIVACY.md", plugin_root / "PRIVACY.md")
    shutil.copy2(ROOT / "TERMS.md", plugin_root / "TERMS.md")

    archive = DIST / f"no-ai-slop-cn-plugin-{manifest['version']}.zip"
    if archive.exists():
        archive.unlink()
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as output:
        for path in sorted(plugin_root.rglob("*")):
            if path.is_file():
                output.write(path, path.relative_to(DIST))
    return plugin_root, archive


def validate_build(plugin_root: Path, archive: Path) -> None:
    expected = {
        ".codex-plugin/plugin.json",
        "assets/no-ai-slop-cn.png",
        "skills/no-ai-slop-cn/SKILL.md",
        "skills/no-ai-slop-cn/agents/openai.yaml",
        "skills/no-ai-slop-cn/eval.md",
        "skills/no-ai-slop-cn/research.md",
        "skills/no-ai-slop-cn/tests.md",
        "LICENSE",
        "PRIVACY.md",
        "TERMS.md",
    }
    actual = {
        path.relative_to(plugin_root).as_posix()
        for path in plugin_root.rglob("*")
        if path.is_file()
    }
    if expected != actual:
        raise SystemExit(
            f"插件文件不符合预期：应为 {sorted(expected)}，"
            f"实际为 {sorted(actual)}"
        )

    skill_root = plugin_root / "skills" / "no-ai-slop-cn"
    for name in SKILL_FILES:
        if (skill_root / name).read_bytes() != (ROOT / name).read_bytes():
            raise SystemExit(f"插件中的 {name} 与规范源文件不一致")
    if (skill_root / "agents" / "openai.yaml").read_bytes() != (
        ROOT / "agents" / "openai.yaml"
    ).read_bytes():
        raise SystemExit("插件中的 agents/openai.yaml 与规范源文件不一致")
    if not zipfile.is_zipfile(archive):
        raise SystemExit("插件压缩包不是有效的 ZIP 文件")
    with zipfile.ZipFile(archive) as packaged:
        archived = set(packaged.namelist())
        damaged = packaged.testzip()
    if damaged is not None:
        raise SystemExit(f"压缩包中的文件校验失败：{damaged}")
    expected_archive = {f"no-ai-slop-cn/{path}" for path in expected}
    if archived != expected_archive:
        raise SystemExit(
            f"压缩包内容不符合预期：应为 {sorted(expected_archive)}，"
            f"实际为 {sorted(archived)}"
        )


def main() -> None:
    args = parse_args()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    validate_source(manifest)
    plugin_root = DIST / "no-ai-slop-cn"
    archive = DIST / f"no-ai-slop-cn-plugin-{manifest['version']}.zip"
    try:
        plugin_root, archive = build_plugin(manifest)
        validate_build(plugin_root, archive)
        print(f"已构建 {archive.relative_to(ROOT)}")
    finally:
        if args.check:
            if plugin_root.exists():
                shutil.rmtree(plugin_root)
            if archive.exists():
                archive.unlink()
            if DIST.exists() and not any(DIST.iterdir()):
                DIST.rmdir()


if __name__ == "__main__":
    main()
