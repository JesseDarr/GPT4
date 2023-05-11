Remove-Item ./logs/ -Recurse -Confirm:$false -ErrorAction SilentlyContinue
Remove-Item ./tests/__pycache__/ -Recurse -Confirm:$false -ErrorAction SilentlyContinue
Remove-Item ./tests/.pytest_cache/ -Recurse -Confirm:$false -ErrorAction SilentlyContinue
Remove-Item ./modules/__pycache__/ -Recurse -Confirm:$false -ErrorAction SilentlyContinue