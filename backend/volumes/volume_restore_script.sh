#!/bin/bash

set -e

# === CONFIG ===
BACKUP_DIR="."  # path to directory with .tar.gz files
declare -A VOLUMES_MAP=(
  ["n8n_data"]="n8n_data.tar.gz"
  ["pgdata_vector"]="pgdata_vector.tar.gz"
  ["minio-data"]="minio-data.tar.gz"
)

# === CHECK ENV ===
if ! command -v docker &> /dev/null; then
  echo "❌ Docker is not installed. Aborting."
  exit 1
fi

echo "📦 Starting restore in: $BACKUP_DIR"
mkdir -p "$BACKUP_DIR"

# === MAIN LOOP ===
for volume in "${!VOLUMES_MAP[@]}"; do
  backup_file="${VOLUMES_MAP[$volume]}"
  full_path="${BACKUP_DIR}/${backup_file}"

  echo -e "\n🧩 Processing volume: $volume"
  if [ ! -f "$full_path" ]; then
    echo "⚠️  volume file not found: $full_path — skipping"
    continue
  fi

  echo "🔍 Creating volume: $volume (if not exists)"
  docker volume create "$volume" > /dev/null

  echo "🔄 Restoring zip into volume..."
  docker run --rm \
    -v "$volume":/data \
    -v "$(realpath "$BACKUP_DIR")":/backup \
    ubuntu bash -c "cd /data && tar xzf /backup/$backup_file"

  echo "✅ Restored: $volume"
done

echo -e "\n🎉 All volumes processed."
