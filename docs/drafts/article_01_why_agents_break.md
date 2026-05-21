---
title: "なぜ私のAIエージェントは3日後に壊れるのか"
emoji: "🔥"
type: "tech"
topics: ["claude", "llm", "ai", "systemd", "python"]
published: false
---

## 3日後に壊れるエージェントの共通点

AIエージェントを作った。動いた。3日後、気づいたら出力が止まっていた。

この経験、心当たりがある人は多いはずだ。

原因は大抵、同じ構造的問題にある。

---

## 「成功したように見えた」問題

```python
result = agent.run(task)
print("Done!")
```

このコードは何も保証していない。`result` はメモリ上の変数だ。プロセスが終わった瞬間に消える。「Done!」と表示されても、有用な出力がディスクに残っているかどうかは別の話だ。

ほとんどのエージェントが3日後に壊れる理由は、**「壊れたこと」を知る仕組みを持っていないから**だ。

---

## 物理証拠主義：ファイルが存在するまで「完了」ではない

解決策はシンプルだ。

> **エージェントの実行は、物理ファイル（証拠）がディスクに存在するまで「完了」と宣言しない。**

```python
def run_with_evidence(task: str) -> pathlib.Path:
    evidence_path = EVIDENCE_DIR / f"evidence_{today}.json"

    # Run the agent
    result = client.messages.create(...)

    # Write evidence FIRST — before declaring done
    evidence_path.write_text(json.dumps({
        "date": today,
        "result": result.content[0].text,
        "tokens": result.usage.output_tokens,
    }))

    # Only NOW can we say "done"
    print(f"Done. Evidence: {evidence_path}")
    return evidence_path
```

ファイルが存在しないなら、実行されていない。これだけだ。

---

## systemdでエージェントを動かす理由

「毎日動かす」を実装するとき、多くの人はこう書く：

```python
while True:
    agent.run()
    time.sleep(86400)
```

これは3日後に別の理由で壊れる（例外、ネットワークエラー、メモリリーク）。

代わりにsystemdを使う。

```ini
# ~/.config/systemd/user/physical-agent.timer
[Timer]
OnCalendar=daily
Persistent=true
```

```bash
systemctl --user enable --now physical-agent.timer
```

systemdはLinuxの枯れたinit systemだ。リトライ、ロギング、失敗検知、依存関係の管理が最初から組み込まれている。LLMエージェントのために車輪を再発明する必要はない。

---

## 免疫ループ：壊れたことを自分で検知する

最後のピース。「壊れても自分で気づく」仕組み。

```python
# violation_detector.py（毎朝6時に実行）
def detect():
    violations = []
    if not today_evidence_exists():
        violations.append({"rule": "stale_evidence", ...})

    # 違反があればClaude APIで修復計画を生成
    if violations:
        repair_plan = call_claude_for_repair(violations)
        write_repair_plan(repair_plan)  # ← これも物理ファイルに残す
```

検知 → 修復計画 → 人間（または次のエージェント）が実行。

この3つのループが揃って初めて、「3日後も動いているエージェントインフラ」になる。

---

## まとめ：3つのパターン

| パターン | 解決する問題 | 実装のコア |
|---------|------------|-----------|
| Physical-First | 実行されたかどうかを証明できない | 証拠ファイルが存在するまで「完了」にしない |
| systemd Runtime | スケジュール実行が不安定 | OSのinit systemを使う |
| Immune Loop | 壊れても気づかない | 違反検知 + AI修復計画の自動化 |

実装は [physical-agent-patterns](https://github.com/aos-standard/physical-agent-patterns) にまとめた。全てのパターンは `anthropic` SDK のみに依存し、フレームワーク不要で動く。モデルは `ANTHROPIC_MODEL` 環境変数で指定可能（デフォルトは `claude-haiku-4-5`）。

これらのパターンの基礎となる思想は [AOS-spec](https://github.com/aos-standard/AOS-spec) に体系化している。エージェントの「許可された操作」と「禁止された操作」を manifest で宣言する軽量な標準だ。
