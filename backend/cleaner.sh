#!/bin/bash

# Function to remove __pycache__ directories
remove_pycache() {
  local dir=$1

  # Find all __pycache__ directories within the given directory
  find "$dir" -type d -name '__pycache__' -exec rm -rf {} +

  echo "Removed all __pycache__ directories within $dir"
}
remove_migrations() {
  local dir=$1

  # Find all migration directories within the given directory
  find "$dir" -type d -name 'migrations' -exec bash -c '
    # Loop through each migration directory
    for mig_dir in "$@"; do
      # Find all files within the migration directory except __init__.py
      files=("$mig_dir"/*)
      for file in "${files[@]}"; do
        if [ "$file" != "$mig_dir/__init__.py" ]; then
          rm -f "$file"
        fi
      done
    done
  ' bash {} +

  echo "Removed all migration files within $dir"
}


# Call the function and provide the target directory as an argument
remove_pycache ./
remove_migrations ./voidcms