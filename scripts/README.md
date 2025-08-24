# Scripts Documentation

このディレクトリには、Segee プロジェクトの管理用スクリプトが含まれています。

## 📜 利用可能なスクリプト

### 1. バージョン管理

#### `update_version.sh`
```bash
./scripts/update_version.sh 0.1.1
```
- `pyproject.toml` のバージョンを更新
- セマンティックバージョニング（x.y.z形式）をチェック
- 安全な更新プロセス

### 2. PyPI 公開

#### `upload_testpypi.sh`
```bash
./scripts/upload_testpypi.sh
```
- Test PyPI への公開
- 全品質チェック（テスト、コード品質、パッケージ整合性）
- 対話式の安全確認

#### `upload_pypi.sh`
```bash
./scripts/upload_pypi.sh
```
- PyPI 本番への公開
- 厳重な確認プロセス（二段階確認）
- 取り返しのつかない操作のため慎重な設計

## 🔄 推奨ワークフロー

### 新バージョンリリース手順

1. **バージョン更新**
   ```bash
   ./scripts/update_version.sh 0.1.1
   ```

2. **変更内容確認**
   ```bash
   git diff
   ```

3. **Test PyPI でテスト**
   ```bash
   ./scripts/upload_testpypi.sh
   ```

4. **インストールテスト**
   ```bash
   pip install --index-url https://test.pypi.org/simple/ segee
   python -c "from segee import SumSegmentTree; print('OK')"
   ```

5. **本番公開**
   ```bash
   ./scripts/upload_pypi.sh
   ```

6. **Git タグ作成**
   ```bash
   git add .
   git commit -m "Release v0.1.1"
   git tag v0.1.1
   git push origin main --tags
   ```

## ⚙️ 事前設定

### PyPI 認証設定
PyPI と Test PyPI の認証設定については、公式ドキュメントを参照：
- [PyPI API Tokens](https://pypi.org/help/#apitoken)
- [Twine Documentation](https://twine.readthedocs.io/en/stable/)

基本的な設定例：
```bash
# ~/.pypirc ファイルに認証情報を設定
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-AgE... # 本番 PyPI のトークン

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-AgE... # Test PyPI のトークン
```

### 必要な依存関係
```bash
uv add --dev build twine
```

## 🛡️ 安全機能

### バージョン管理
- セマンティックバージョニングの強制
- 現在バージョンと新バージョンの明示
- 対話式確認

### Test PyPI
- 全品質チェック実行
- パッケージ整合性検証
- 継続確認

### 本番 PyPI
- 二段階確認プロセス
- バージョン重複防止警告
- 明示的な "yes" 入力要求

## 🚨 注意事項

1. **本番 PyPI は取り消し不可**
   - 一度公開したバージョンは削除できません
   - 必ず Test PyPI でテストしてください

2. **バージョンの重複禁止**
   - 同じバージョン番号で再公開できません
   - バージョンアップが必要です

3. **認証情報の管理**
   - API Token は絶対に公開しない
   - `~/.pypirc` のファイル権限は 600 に設定

## 🔍 トラブルシューティング

### よくあるエラー

#### "File already exists"
```bash
# バージョンを上げて再実行
./scripts/update_version.sh 0.1.2
./scripts/upload_pypi.sh
```

#### 認証エラー
```bash
# 認証設定を確認
cat ~/.pypirc
ls -la ~/.pypirc  # 権限確認（600 であること）
```

#### テストエラー
```bash
# 個別にテスト実行
uv run pytest -v
uv run ruff check segee/
```

## 📊 スクリプト実行例

```bash
# 完全なリリースフロー
./scripts/update_version.sh 0.2.0
./scripts/upload_testpypi.sh
# テスト後...
./scripts/upload_pypi.sh
```
