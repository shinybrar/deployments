#!/bin/sh

if [ -d "$USER_DATASETS_ROOT_PATH" ]; then
  for DATASET in $(find "$USER_DATASETS_ROOT_PATH" -maxdepth 1); do
    ln -sf "$DATASET" "$HOME"
  done
  rm "$HOME/$(basename "$USER_DATASETS_ROOT_PATH")"
else
  echo "$USER_DATASETS_ROOT_PATH directory does not exist."
fi