#!/bin/bash
# Test PyPI 公開スクリプト

set -e

echo "🚀 Segee Test PyPI アップロード開始"

# 1. テスト実行
echo "📝 テスト実行中..."
uv run pytest

# 2. コード品質チェック
echo "✨ コード品質チェック中..."
uv run ruff check segee/
uv run ruff format --check segee/

# 3. 既存のビルドファイルを削除
echo "🧹 古いビルドファイルを削除..."
rm -rf dist/ build/ *.egg-info/

# 4. パッケージビルド
echo "📦 パッケージビルド中..."
uv run python -m build

# 5. パッケージチェック
echo "🔍 パッケージ整合性チェック..."
uv run twine check dist/*

# 6. Test PyPI にアップロード
echo "🌐 Test PyPI にアップロード中..."
echo "注意: ~/.pypirc にTest PyPI の認証情報が設定されていることを確認してください"
read -p "続行しますか？ (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    uv run twine upload --repository testpypi dist/*
    echo "✅ アップロード完了！"
    echo "📋 Test PyPI: https://test.pypi.org/project/segee/"
    echo "💾 インストールテスト: pip install --index-url https://test.pypi.org/simple/ segee"
else
    echo "❌ アップロードをキャンセルしました"
fi
