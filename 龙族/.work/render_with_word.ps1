param([string]$QaFolder = 'qa_round2')
$ErrorActionPreference = 'Stop'
$taskRoot = Split-Path -Parent $PSScriptRoot
$qaDir = Join-Path $PSScriptRoot $QaFolder
New-Item -ItemType Directory -Path $qaDir -Force | Out-Null
$taskManifest = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'manifest.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$taskDocPath = Join-Path $taskRoot $taskManifest.books[0].working_docx
$taskPdfPath = Join-Path $qaDir 'working-draft.pdf'
$wordApp = $null
$taskDoc = $null
try {
    $wordApp = New-Object -ComObject Word.Application
    $wordApp.Visible = $false
    $wordApp.DisplayAlerts = 0
    $taskDoc = $wordApp.Documents.Open($taskDocPath, $false, $true)
    $taskDoc.Repaginate()
    $taskDoc.ExportAsFixedFormat($taskPdfPath, 17)
    Write-Output "PDF exported: $taskPdfPath"
    Write-Output "Pages: $($taskDoc.ComputeStatistics(2))"
} finally {
    if ($null -ne $taskDoc) { $taskDoc.Close(0); [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($taskDoc) }
    if ($null -ne $wordApp) { $wordApp.Quit(); [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($wordApp) }
}
