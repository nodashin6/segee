#!/bin/bash
# PyPI 本番公開スクリプト

set -e

echo "🚀 Segee PyPI 本番アップロード開始"

# バージョンチェック
echo "📋 現在のバージョンを確認..."
current_version=$(grep 'version = ' pyproject.toml | cut -d'"' -f2)
echo "現在のバージョン: $current_version"

# バージョン確認の警告
echo "⚠️  注意: PyPI本番では一度公開したバージョンは削除できません！"
echo "バージョン $current_version で公開します。"
read -p "このバージョンで本当に公開しますか？ (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ 公開をキャンセルしました"
    echo "💡 ヒント: pyproject.toml でバージョンを変更してください"
    exit 1
fi

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

# 6. PyPI 本番にアップロード
echo "🌐 PyPI 本番にアップロード中..."
echo "注意: ~/.pypirc にPyPI 本番の認証情報が設定されていることを確認してください"
echo "または、TWINE_USERNAME と TWINE_PASSWORD 環境変数が設定されていることを確認してください"
echo ""
echo "最後の確認: バージョン $current_version を PyPI 本番に公開します"
read -p "本当に続行しますか？ (yes と入力してください): " confirm

if [[ "$confirm" == "yes" ]]; then
    uv run twine upload dist/*
    echo "✅ アップロード完了！"
    echo "📋 PyPI: https://pypi.org/project/segee/"
    echo "💾 インストール: pip install segee"
    echo "🎉 おめでとうございます！パッケージが世界中で利用可能になりました！"
else
    echo "❌ アップロードをキャンセルしました"
    echo "💡 本番公開するには 'yes' と正確に入力してください"
fi
