$ErrorActionPreference = 'Stop'
$taskBuild = Join-Path $env:TEMP 'codex-complex-midterm'
if ($taskBuild -match '[^\x00-\x7F]') { throw '临时编译目录必须为纯ASCII路径' }
New-Item -ItemType Directory -Path $taskBuild -Force | Out-Null
$sourceDir = $PSScriptRoot
$outputDir = Split-Path -Parent $sourceDir
$logDir = Join-Path $sourceDir 'build'
New-Item -ItemType Directory -Path $logDir -Force | Out-Null
$jobs = @(
    @{ Entry = 'notes'; Output = '复分析期中考试重点.pdf' },
    @{ Entry = 'exercises'; Output = '复分析期中练习100题.pdf' }
)
foreach ($job in $jobs) {
    $entry = $job.Entry
    Copy-Item -LiteralPath (Join-Path $sourceDir ($entry + '.tex')) -Destination (Join-Path $taskBuild ($entry + '.tex')) -Force
    Push-Location $taskBuild
    try {
        for ($pass = 1; $pass -le 3; $pass++) {
            & xelatex -interaction=nonstopmode -halt-on-error -file-line-error ($entry + '.tex') > ($entry + '-pass' + $pass + '.txt')
            if ($LASTEXITCODE -ne 0) { throw "编译失败：$entry，第$pass 遍；日志位于 $taskBuild" }
        }
    } finally { Pop-Location }
    Copy-Item -LiteralPath (Join-Path $taskBuild ($entry + '.pdf')) -Destination (Join-Path $outputDir $job.Output) -Force
    foreach ($extension in @('log','aux','toc','out')) {
        $candidate = Join-Path $taskBuild ($entry + '.' + $extension)
        if (Test-Path -LiteralPath $candidate) { Copy-Item -LiteralPath $candidate -Destination $logDir -Force }
    }
    Write-Output ('已编译：' + (Join-Path $outputDir $job.Output))
}
