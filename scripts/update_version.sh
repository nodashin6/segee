#!/bin/bash
# バージョン更新スクリプト

set -e

if [ $# -eq 0 ]; then
    echo "使用方法: $0 <new_version>"
    echo "例: $0 0.1.1"
    echo "例: $0 0.2.0"
    exit 1
fi

NEW_VERSION="$1"

# バージョン形式チェック
if [[ ! $NEW_VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "❌ エラー: バージョンは x.y.z 形式で指定してください"
    echo "例: 0.1.1, 1.0.0"
    exit 1
fi

# 現在のバージョンを取得
CURRENT_VERSION=$(grep 'version = ' pyproject.toml | cut -d'"' -f2)

echo "📋 バージョン更新"
echo "現在: $CURRENT_VERSION"
echo "新規: $NEW_VERSION"

# 確認
read -p "バージョンを更新しますか？ (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ キャンセルしました"
    exit 1
fi

# pyproject.toml のバージョンを更新
sed -i "s/version = \"$CURRENT_VERSION\"/version = \"$NEW_VERSION\"/" pyproject.toml

echo "✅ バージョンを $NEW_VERSION に更新しました"
echo ""
echo "次のステップ:"
echo "1. 変更内容を確認: git diff"
echo "2. テスト実行: uv run pytest"
echo "3. Test PyPI に公開: ./scripts/upload_testpypi.sh"
echo "4. 問題なければ本番公開: ./scripts/upload_pypi.sh"
