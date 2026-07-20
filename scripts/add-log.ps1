param(
    [Parameter(Mandatory = $true)]
    [string]$Text,

    [string]$Category = "随手记"
)

$ErrorActionPreference = "Stop"
$repositoryRoot = Split-Path -Parent $PSScriptRoot

Push-Location $repositoryRoot
try {
    $entryPath = & python scripts/add_entry.py --text $Text --category $Category
    if ($LASTEXITCODE -ne 0) {
        throw "创建学习记录失败。"
    }

    git add -- $entryPath
    git diff --cached --quiet
    if ($LASTEXITCODE -eq 0) {
        Write-Host "今天的相同记录已经存在，没有生成新提交。"
        return
    }

    $entryDate = [System.IO.Path]::GetFileNameWithoutExtension($entryPath)
    git commit -m "log: record $entryDate learning entry"
    if ($LASTEXITCODE -ne 0) {
        throw "提交学习记录失败。"
    }

    git push
    if ($LASTEXITCODE -ne 0) {
        throw "推送学习记录失败；本地提交已保留。"
    }

    Write-Host "已记录：$entryPath"
}
finally {
    Pop-Location
}
